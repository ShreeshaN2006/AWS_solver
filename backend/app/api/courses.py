from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any, Optional
from app.database import get_database

router = APIRouter(prefix="/api/courses", tags=["Courses"])

@router.get("/183194")
async def get_course_details():
    """Retrieve full AWS Academy Cloud Foundations course information."""
    db = get_database()
    course = await db.courses.find_one({"course_id": "183194"}, {"_id": 0})
    if not course:
        # Fallback if seed not run yet
        from app.seed_data.course_seed import COURSE_SEED_MODULES
        return {
            "course_id": "183194",
            "name": "AWS Academy Cloud Foundations",
            "code": "ACF-183194",
            "canvas_url": "https://awsacademy.instructure.com/courses/183194/modules",
            "total_modules": 10,
            "modules": COURSE_SEED_MODULES
        }
    return course

@router.get("/183194/modules")
async def get_modules(core_only: bool = Query(False, description="Filter for 10 core modules only")):
    """List all modules or just core 10 modules with progress and items."""
    db = get_database()
    q = {"course_id": "183194"}
    if core_only:
        q["is_core_module"] = True
    
    modules = []
    async for m in db.modules.find(q, {"_id": 0}).sort("order", 1):
        modules.append(m)
    return modules

@router.get("/183194/modules/{module_id}")
async def get_module_by_id(module_id: str):
    """Retrieve detailed content, items, and lab associations for a module."""
    db = get_database()
    mod = await db.modules.find_one({"course_id": "183194", "module_id": module_id}, {"_id": 0})
    if not mod:
        raise HTTPException(status_code=404, detail=f"Module {module_id} not found.")
    return mod
