from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any, Optional
from app.services.canvas_api import canvas_service
from app.config import settings

router = APIRouter(prefix="/api/canvas", tags=["Canvas LMS Integration"])

@router.get("/status")
async def get_canvas_status():
    """Check Canvas LMS connection status and credentials."""
    conn_result = await canvas_service.test_connection()
    return {
        "base_url": settings.CANVAS_BASE_URL,
        "course_id": settings.CANVAS_COURSE_ID,
        "has_token": bool(settings.CANVAS_API_TOKEN),
        "test_result": conn_result,
        "mode": "Live REST API" if conn_result.get("connected") else "Local Document & HTML Fallback"
    }

@router.post("/sync")
async def sync_canvas_modules():
    """
    Authorized read-only synchronization of modules and assignments from Canvas API.
    Strictly read-only: never alters grades or submits student assessments.
    """
    modules = await canvas_service.fetch_course_modules(course_id=settings.CANVAS_COURSE_ID)
    if not modules:
        return {
            "status": "fallback_active",
            "message": "Canvas API token not set or live server unreachable. Retaining local course catalog.",
            "synced_count": 0
        }
    
    return {
        "status": "success",
        "synced_count": len(modules),
        "message": f"Successfully pulled {len(modules)} modules from Canvas LMS."
    }
