from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class Citation(BaseModel):
    module_id: Optional[str] = None
    module_title: Optional[str] = None
    document_name: str
    page_number: Optional[int] = None
    timestamp: Optional[str] = None
    source_url: Optional[str] = None
    snippet: str
    confidence: float = 0.0

class ChatMessage(BaseModel):
    message_id: str
    session_id: str
    role: str  # "user", "assistant", "system"
    content: str
    citations: List[Citation] = []
    tool_calls: Optional[List[Dict[str, Any]]] = None
    module_context: Optional[str] = None
    lesson_context: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ChatSession(BaseModel):
    session_id: str
    user_id: str = "default_student"
    title: str = "AWS Study Session"
    current_module_id: Optional[str] = None
    current_lesson_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    messages: List[ChatMessage] = []

class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    message: str
    module_id: Optional[str] = None
    lesson_id: Optional[str] = None
    provider: Optional[str] = None

class ChatResponse(BaseModel):
    session_id: str
    message: str
    citations: List[Citation] = []
    suggested_followups: List[str] = []
    used_tools: List[str] = []
