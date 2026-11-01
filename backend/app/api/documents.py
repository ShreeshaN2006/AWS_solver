from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Query
from typing import List, Dict, Any, Optional
import os
from app.database import get_database
from app.services.ingestion import ingestion_service

router = APIRouter(prefix="/api/documents", tags=["Course Knowledge Base & Documents"])

@router.get("")
async def list_documents(course_id: str = "183194"):
    """List all indexed learning documents."""
    db = get_database()
    docs = []
    async for d in db.learning_documents.find({"course_id": course_id}, {"_id": 0}).sort("uploaded_at", -1):
        docs.append(d)
    return docs

@router.get("/chunks")
async def list_chunks(
    module_id: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=100)
):
    """Retrieve indexed document chunks with vector embeddings and source metadata."""
    db = get_database()
    q = {"course_id": "183194"}
    if module_id and module_id != "all":
        q["module_id"] = str(module_id)

    chunks = []
    async for c in db.document_chunks.find(q, {"_id": 0, "embedding": 0}).limit(limit):
        chunks.append(c)
    return chunks

@router.post("/import-canvas-html")
async def import_canvas_html(file: UploadFile = File(...)):
    """
    Import Canvas course modules HTML export.
    Parses module titles, IDs, items, links, and structure.
    """
    content = await file.read()
    html_text = content.decode("utf-8", errors="replace")
    
    result = await ingestion_service.parse_canvas_html(html_text, course_id="183194")
    return {
        "status": "success",
        "filename": file.filename,
        "details": result,
        "message": "Canvas HTML course export parsed and cataloged successfully."
    }

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    module_id: str = Form(...),
    module_title: str = Form(...),
    doc_type: str = Form("pdf")
):
    """
    Upload a course PDF, student guide, or video transcript.
    Extracts text, splits into semantic chunks, generates embeddings, and saves to vector index.
    """
    content = await file.read()
    filename = file.filename or "uploaded_doc"

    if doc_type == "pdf" or filename.lower().endswith(".pdf"):
        result = await ingestion_service.process_pdf_document(
            pdf_bytes=content,
            filename=filename,
            module_id=module_id,
            module_title=module_title,
            course_id="183194"
        )
    else:
        text_str = content.decode("utf-8", errors="replace")
        result = await ingestion_service.process_transcript_or_text(
            text_content=text_str,
            filename=filename,
            module_id=module_id,
            module_title=module_title,
            course_id="183194"
        )

    return {
        "status": "success",
        "filename": filename,
        "details": result,
        "message": f"Successfully processed and indexed {result.get('chunks_created', 0)} chunks for RAG."
    }
