from fastapi import APIRouter, HTTPException, Body
from typing import List, Dict, Any, Optional
from app.services.planner_service import planner_service
from app.models.planner import GeneratePlanRequest, StudyPlan
from app.database import get_database

router = APIRouter(prefix="/api/planner", tags=["Study Planner"])

@router.get("/current")
async def get_current_study_plan(user_id: str = "default_student", course_id: str = "183194"):
    """Retrieve active adaptive study plan and daily schedule."""
    plan = await planner_service.get_current_plan(user_id=user_id, course_id=course_id)
    return plan

@router.post("/generate", response_model=StudyPlan)
async def generate_new_study_plan(req: GeneratePlanRequest, user_id: str = "default_student", course_id: str = "183194"):
    """
    Synthesize an updated study plan based on remaining modules,
    unfinished labs, and weak topics identified from practice attempts.
    """
    return await planner_service.generate_study_plan(req, user_id=user_id, course_id=course_id)

@router.post("/task/{task_id}/toggle")
async def toggle_task_completion(task_id: str, completed: bool = Body(..., embed=True), user_id: str = "default_student", course_id: str = "183194"):
    """Toggle completion status for a specific study task in the daily schedule."""
    db = get_database()
    plan = await db.study_plans.find_one({"user_id": user_id, "course_id": course_id})
    if not plan:
        raise HTTPException(status_code=404, detail="Study plan not found.")

    updated = False
    for day in plan.get("schedules", []):
        for task in day.get("tasks", []):
            if task.get("task_id") == task_id:
                task["is_completed"] = completed
                updated = True
                break
        if updated:
            break

    if updated:
        await db.study_plans.update_one(
            {"user_id": user_id, "course_id": course_id},
            {"$set": {"schedules": plan["schedules"]}}
        )
    return {"task_id": task_id, "is_completed": completed}
