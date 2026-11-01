from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any, Optional
from app.database import get_database
from app.models.chat import ChatRequest, ChatResponse
from app.services.agent import copilot_agent

router = APIRouter(prefix="/api/chat", tags=["AI Tutor"])

@router.post("/message", response_model=ChatResponse)
async def send_chat_message(req: ChatRequest):
    """
    Interact with the AWS Academy AI Tutor.
    Grounds explanations in course material, provides source citations, and routes tool requests.
    """
    result = await copilot_agent.process_chat(
        user_message=req.message,
        session_id=req.session_id,
        module_id=req.module_id,
        lesson_id=req.lesson_id
    )
    return ChatResponse(**result)

@router.get("/sessions")
async def list_chat_sessions(user_id: str = "default_student"):
    """Retrieve prior study chat sessions for the user."""
    db = get_database()
    sessions = []
    async for s in db.chat_sessions.find({"user_id": user_id}, {"_id": 0}).sort("updated_at", -1):
        sessions.append(s)
    return sessions

@router.get("/sessions/{session_id}/messages")
async def get_session_messages(session_id: str):
    """Retrieve chat history with citations for a specific study session."""
    db = get_database()
    messages = []
    async for m in db.chat_messages.find({"session_id": session_id}, {"_id": 0}).sort("created_at", 1):
        messages.append(m)
    return messages
