from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class DocumentChunk(BaseModel):
    chunk_id: str
    doc_id: str
    course_id: str = "183194"
    module_id: str
    module_title: str
    learning_item_id: Optional[str] = None
    document_name: str
    page_number: Optional[int] = None
    timestamp: Optional[str] = None
    content: str
    embedding: Optional[List[float]] = None
    source_url: Optional[str] = None
    token_count: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)

class LearningDocument(BaseModel):
    doc_id: str
    course_id: str = "183194"
    module_id: str
    module_title: str
    title: str
    file_type: str  # "pdf", "html", "transcript", "text", "guide"
    original_filename: str
    file_size_bytes: int = 0
    chunk_count: int = 0
    source_url: Optional[str] = None
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    processed: bool = False
