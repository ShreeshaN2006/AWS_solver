from typing import Optional

from fastapi import APIRouter, Body, HTTPException

from app.config import settings
from app.services.llm_provider import get_llm_provider

router = APIRouter(prefix="/api/settings", tags=["Settings & Configuration"])


@router.get("")
async def get_system_settings():
    """Return non-secret configuration metadata; never expose connection URIs or tokens."""
    return {
        "llm_provider": settings.LLM_PROVIDER,
        "openai_model": settings.OPENAI_MODEL,
        "openai_has_key": bool(settings.OPENAI_API_KEY),
        "bedrock_model_id": settings.BEDROCK_MODEL_ID,
        "bedrock_region": settings.AWS_REGION,
        "bedrock_has_credentials": bool(
            settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY
        ),
        "bedrock_uses_default_credential_chain": not bool(
            settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY
        ),
        "canvas_base_url": settings.CANVAS_BASE_URL,
        "canvas_course_id": settings.CANVAS_COURSE_ID,
        "canvas_has_token": bool(settings.CANVAS_API_TOKEN),
        "mongodb_configured": bool(settings.MONGODB_URI),
        "mongodb_db": settings.MONGODB_DB_NAME,
    }


@router.post("/provider")
async def update_llm_provider(
    provider: str = Body(..., embed=True),
    openai_key: Optional[str] = Body(None, embed=True),
    aws_key: Optional[str] = Body(None, embed=True),
    aws_secret: Optional[str] = Body(None, embed=True),
):
    """Switch providers after validating configuration; secrets are held in memory only."""
    p_clean = provider.lower().strip()
    if p_clean not in ["local_mock", "openai", "bedrock"]:
        raise HTTPException(
            status_code=400,
            detail="Provider must be one of: local_mock, openai, bedrock",
        )

    if bool(aws_key) != bool(aws_secret):
        raise HTTPException(
            status_code=400,
            detail="Provide both AWS access key and secret, or leave both blank to use the AWS credential chain.",
        )

    previous_openai_key = settings.OPENAI_API_KEY
    previous_aws_key = settings.AWS_ACCESS_KEY_ID
    previous_aws_secret = settings.AWS_SECRET_ACCESS_KEY

    if openai_key:
        settings.OPENAI_API_KEY = openai_key
    if aws_key and aws_secret:
        settings.AWS_ACCESS_KEY_ID = aws_key
        settings.AWS_SECRET_ACCESS_KEY = aws_secret

    try:
        # OpenAI initialization verifies that a key is present. Bedrock can use
        # the AWS SDK default chain, including SSO or an attached IAM role.
        get_llm_provider(p_clean)
    except Exception as exc:
        settings.OPENAI_API_KEY = previous_openai_key
        settings.AWS_ACCESS_KEY_ID = previous_aws_key
        settings.AWS_SECRET_ACCESS_KEY = previous_aws_secret
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    settings.LLM_PROVIDER = p_clean

    return {
        "status": "success",
        "active_provider": settings.LLM_PROVIDER,
        "message": (
            f"AI provider switched to {settings.LLM_PROVIDER}. "
            "Provider settings and submitted keys apply to this running backend process only. "
            "Re-index documents after switching providers because embedding spaces may differ."
        ),
    }
