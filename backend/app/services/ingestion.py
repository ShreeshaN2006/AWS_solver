import uuid
import re
import logging
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional
import pymupdf as fitz  # PyMuPDF
from app.database import get_database
from app.services.vector_store import vector_store

logger = logging.getLogger("app.services.ingestion")

class DocumentIngestionService:
    @staticmethod
    def chunk_text(
        text: str,
        chunk_size: int = 800,
        chunk_overlap: int = 150
    ) -> List[str]:
        """Split text into overlapping chunks cleanly on sentence or paragraph boundaries."""
        clean_text = re.sub(r'\s+', ' ', text).strip()
        if not clean_text:
            return []
        
        chunks = []
        start = 0
        text_length = len(clean_text)

        while start < text_length:
            end = start + chunk_size
            if end >= text_length:
                chunks.append(clean_text[start:].strip())
                break
            
            # Find closest sentence end or whitespace before `end`
            split_at = clean_text.rfind('. ', start, end)
            if split_at != -1 and split_at > start + (chunk_size // 2):
                end = split_at + 1
            else:
                space_at = clean_text.rfind(' ', start, end)
                if space_at != -1 and space_at > start + (chunk_size // 2):
                    end = space_at

            chunk = clean_text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            start = end - chunk_overlap
            if start < 0 or start >= text_length:
                break
                
        return chunks

    @classmethod
    async def parse_canvas_html(cls, html_content: str, course_id: str = "183194") -> Dict[str, Any]:
        """
        Parses Canvas LMS modules HTML export:
        Extracts modules, IDs, item titles, types, URLs.
        Updates MongoDB collections: `courses`, `modules`, `module_items`.
        """
        db = get_database()
        soup = BeautifulSoup(html_content, "html.parser")
        
        modules_data = []
        module_elements = soup.find_all("div", class_=lambda c: c and "context_module" in c)
        
        order = 1
        for mod_elem in module_elements:
            module_id = mod_elem.get("data-module-id") or mod_elem.get("id", "").replace("context_module_", "")
            if not module_id:
                module_id = f"mod_{order}"

            # Extract module title
            header_span = mod_elem.find("span", class_="name")
            title = header_span.get_text(strip=True) if header_span else f"Module {order}"
            
            # Determine module number
            module_num = 0
            is_core = False
            match = re.search(r"Module\s+(\d+)", title, re.IGNORECASE)
            if match:
                module_num = int(match.group(1))
                is_core = True

            # Extract module items
            items = []
            item_elements = mod_elem.find_all("li", class_=lambda c: c and "ig-row" in c)
            item_pos = 1
            for item_elem in item_elements:
                item_id = item_elem.get("data-item-id") or f"item_{module_id}_{item_pos}"
                title_link = item_elem.find("a", class_="ig-title")
                item_title = title_link.get_text(strip=True) if title_link else "Untitled Item"
                href = title_link.get("href") if title_link else None

                type_span = item_elem.find("span", class_="type-msg")
                item_type = type_span.get_text(strip=True) if type_span else "Page"

                items.append({
                    "item_id": str(item_id),
                    "module_id": str(module_id),
                    "title": item_title,
                    "type": item_type,
                    "url": href,
                    "position": item_pos,
                    "is_completed": False,
                    "time_estimate_mins": 20 if "Lab" in item_title else (15 if "Quiz" in item_title else 10)
                })
                item_pos += 1

            has_lab = any("lab" in it["title"].lower() for it in items)
            lab_id = None
            if has_lab:
                lab_id = f"lab_{module_num}"

            mod_record = {
                "module_id": str(module_id),
                "course_id": course_id,
                "module_number": module_num,
                "title": title,
                "is_core_module": is_core,
                "order": order,
                "items": items,
                "progress_percentage": 0.0,
                "status": "Not Started",
                "has_lab": has_lab,
                "lab_id": lab_id
            }

            # Upsert into MongoDB
            await db.modules.update_one(
                {"course_id": course_id, "module_id": str(module_id)},
                {"$set": mod_record},
                upsert=True
            )
            modules_data.append(mod_record)
            order += 1

        # Upsert Course record
        course_record = {
            "course_id": course_id,
            "name": "AWS Academy Cloud Foundations",
            "code": "ACF-183194",
            "canvas_url": f"https://awsacademy.instructure.com/courses/{course_id}/modules",
            "total_modules": len([m for m in modules_data if m["is_core_module"]]),
            "module_count_total": len(modules_data),
            "modules": modules_data
        }
        await db.courses.update_one(
            {"course_id": course_id},
            {"$set": course_record},
            upsert=True
        )

        return {
            "course_id": course_id,
            "modules_imported": len(modules_data),
            "total_items": sum(len(m["items"]) for m in modules_data)
        }

    @classmethod
    async def process_pdf_document(
        cls,
        pdf_bytes: bytes,
        filename: str,
        module_id: str,
        module_title: str,
        course_id: str = "183194",
        source_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """Extract text per page using PyMuPDF and generate vectorized chunks."""
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        doc_id = f"doc_{uuid.uuid4().hex[:12]}"
        all_chunks = []
        page_count = len(doc)

        for page_idx in range(page_count):
            page = doc.load_page(page_idx)
            text = page.get_text("text")
            if not text.strip():
                continue
            
            raw_chunks = cls.chunk_text(text, chunk_size=800, chunk_overlap=120)
            for chunk_str in raw_chunks:
                chunk_id = f"chk_{uuid.uuid4().hex[:12]}"
                all_chunks.append({
                    "chunk_id": chunk_id,
                    "doc_id": doc_id,
                    "course_id": course_id,
                    "module_id": str(module_id),
                    "module_title": module_title,
                    "document_name": filename,
                    "page_number": page_idx + 1,
                    "content": chunk_str,
                    "source_url": source_url,
                    "token_count": len(chunk_str.split())
                })

        # Save document record
        db = get_database()
        doc_record = {
            "doc_id": doc_id,
            "course_id": course_id,
            "module_id": str(module_id),
            "module_title": module_title,
            "title": filename.replace(".pdf", "").replace("-", " ").title(),
            "file_type": "pdf",
            "original_filename": filename,
            "file_size_bytes": len(pdf_bytes),
            "chunk_count": len(all_chunks),
            "source_url": source_url,
            "processed": True
        }
        await db.learning_documents.update_one({"doc_id": doc_id}, {"$set": doc_record}, upsert=True)

        # Index vectors
        indexed = await vector_store.add_chunks(all_chunks)
        return {"doc_id": doc_id, "pages": page_count, "chunks_created": indexed}

    @classmethod
    async def process_transcript_or_text(
        cls,
        text_content: str,
        filename: str,
        module_id: str,
        module_title: str,
        course_id: str = "183194",
        source_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """Extract text chunks with timestamp detection (e.g. [02:45] or 02:45)."""
        doc_id = f"doc_{uuid.uuid4().hex[:12]}"
        all_chunks = []

        # Parse timestamp segments if present
        timestamp_blocks = re.split(r'(\[\d{1,2}:\d{2}(?::\d{2})?\]|\b\d{1,2}:\d{2}\b)', text_content)
        if len(timestamp_blocks) > 3:
            current_timestamp = "00:00"
            for i in range(1, len(timestamp_blocks), 2):
                current_timestamp = timestamp_blocks[i].strip("[]")
                segment_text = timestamp_blocks[i+1] if (i+1) < len(timestamp_blocks) else ""
                for chunk_str in cls.chunk_text(segment_text, chunk_size=700, chunk_overlap=100):
                    all_chunks.append({
                        "chunk_id": f"chk_{uuid.uuid4().hex[:12]}",
                        "doc_id": doc_id,
                        "course_id": course_id,
                        "module_id": str(module_id),
                        "module_title": module_title,
                        "document_name": filename,
                        "timestamp": current_timestamp,
                        "content": chunk_str,
                        "source_url": source_url,
                        "token_count": len(chunk_str.split())
                    })
        else:
            raw_chunks = cls.chunk_text(text_content, chunk_size=800, chunk_overlap=120)
            for chunk_str in raw_chunks:
                all_chunks.append({
                    "chunk_id": f"chk_{uuid.uuid4().hex[:12]}",
                    "doc_id": doc_id,
                    "course_id": course_id,
                    "module_id": str(module_id),
                    "module_title": module_title,
                    "document_name": filename,
                    "content": chunk_str,
                    "source_url": source_url,
                    "token_count": len(chunk_str.split())
                })

        db = get_database()
        doc_record = {
            "doc_id": doc_id,
            "course_id": course_id,
            "module_id": str(module_id),
            "module_title": module_title,
            "title": filename.replace(".txt", "").replace("-", " ").title(),
            "file_type": "transcript" if "transcript" in filename.lower() else "text",
            "original_filename": filename,
            "file_size_bytes": len(text_content.encode("utf-8")),
            "chunk_count": len(all_chunks),
            "source_url": source_url,
            "processed": True
        }
        await db.learning_documents.update_one({"doc_id": doc_id}, {"$set": doc_record}, upsert=True)

        indexed = await vector_store.add_chunks(all_chunks)
        return {"doc_id": doc_id, "chunks_created": indexed}

ingestion_service = DocumentIngestionService()
