from fastapi import APIRouter, HTTPException, Body
from typing import List, Dict, Any, Optional
from app.services.planner_service import planner_service

router = APIRouter(prefix="/api/progress", tags=["Progress & Analytics"])

@router.get("/analytics")
async def get_progress_analytics(user_id: str = "default_student", course_id: str = "183194"):
    """
    Get aggregated progress analytics across all 10 modules, labs, and quizzes.
    Includes weak topics, understood concepts, recent activities, and upcoming tasks.
    """
    return await planner_service.get_overall_progress(user_id=user_id, course_id=course_id)

@router.post("/item")
async def update_item_progress(
    module_id: str = Body(...),
    item_id: str = Body(...),
    completed: bool = Body(...),
    time_spent_mins: int = Body(15),
    user_id: str = Body("default_student"),
    course_id: str = Body("183194")
):
    """
    Update local completion status of a module learning resource.
    Preserves distinction between local progress and official Canvas LMS grading.
    """
    return await planner_service.record_item_progress(
        user_id=user_id,
        course_id=course_id,
        module_id=module_id,
        item_id=item_id,
        completed=completed,
        time_spent_mins=time_spent_mins
    )
