from fastapi import APIRouter, HTTPException, Body
from typing import List, Dict, Any, Optional
from app.config import settings
from app.services.llm_provider import get_llm_provider

router = APIRouter(prefix="/api/settings", tags=["Settings & Configuration"])

@router.get("")
async def get_system_settings():
    """Retrieve active system configuration and AI provider status."""
    return {
        "llm_provider": settings.LLM_PROVIDER,
        "openai_model": settings.OPENAI_MODEL,
        "openai_has_key": bool(settings.OPENAI_API_KEY),
        "bedrock_model_id": settings.BEDROCK_MODEL_ID,
        "bedrock_region": settings.AWS_REGION,
        "bedrock_has_credentials": bool(settings.AWS_ACCESS_KEY_ID),
        "canvas_base_url": settings.CANVAS_BASE_URL,
        "canvas_course_id": settings.CANVAS_COURSE_ID,
        "canvas_has_token": bool(settings.CANVAS_API_TOKEN),
        "mongodb_uri": settings.MONGODB_URI,
        "mongodb_db": settings.MONGODB_DB_NAME
    }

@router.post("/provider")
async def update_llm_provider(
    provider: str = Body(..., embed=True),
    openai_key: Optional[str] = Body(None, embed=True),
    aws_key: Optional[str] = Body(None, embed=True),
    aws_secret: Optional[str] = Body(None, embed=True)
):
    """Dynamically switch between 'local_mock', 'openai', and 'bedrock'."""
    p_clean = provider.lower().strip()
    if p_clean not in ["local_mock", "openai", "bedrock"]:
        raise HTTPException(status_code=400, detail="Provider must be one of: local_mock, openai, bedrock")

    settings.LLM_PROVIDER = p_clean
    if openai_key:
        settings.OPENAI_API_KEY = openai_key
    if aws_key:
        settings.AWS_ACCESS_KEY_ID = aws_key
    if aws_secret:
        settings.AWS_SECRET_ACCESS_KEY = aws_secret

    return {
        "status": "success",
        "active_provider": settings.LLM_PROVIDER,
        "message": f"AI provider successfully switched to {settings.LLM_PROVIDER}."
    }
