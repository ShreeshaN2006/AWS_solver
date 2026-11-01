from pathlib import Path
from typing import Iterable

import fitz
from bs4 import BeautifulSoup

from app.models.schemas import DocumentChunk
from app.services.embeddings import embed_text


class DocumentIngestionService:
    @staticmethod
    def extract_text_from_pdf(file_path: Path) -> list[tuple[int, str]]:
        pages: list[tuple[int, str]] = []
        with fitz.open(file_path) as doc:
            for idx, page in enumerate(doc, start=1):
                text = page.get_text().strip()
                if text:
                    pages.append((idx, text))
        return pages

    @staticmethod
    def extract_text_from_html(html_content: str) -> str:
        soup = BeautifulSoup(html_content, "html.parser")
        return " ".join(soup.get_text(" ").split())

    @staticmethod
    def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> Iterable[str]:
        words = text.split()
        if not words:
            return []
        chunks = []
        start = 0
        while start < len(words):
            end = min(len(words), start + chunk_size)
            chunks.append(" ".join(words[start:end]))
            if end == len(words):
                break
            start = max(0, end - overlap)
        return chunks

    def build_chunks(
        self,
        *,
        course_id: int,
        module_id: str,
        module_title: str,
        document_name: str,
        text: str,
        learning_item_id: str | None = None,
        source_url: str | None = None,
    ) -> list[DocumentChunk]:
        chunks = []
        for part in self.chunk_text(text):
            chunks.append(
                DocumentChunk(
                    course_id=course_id,
                    module_id=module_id,
                    module_title=module_title,
                    learning_item_id=learning_item_id,
                    document_name=document_name,
                    extracted_content=part,
                    embedding=embed_text(part),
                    source_url=source_url,
                )
            )
        return chunks
