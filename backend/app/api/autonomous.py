from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any, Dict

from app.config import settings
from app.services.autonomous_agent import get_autonomous_agent

router = APIRouter(prefix="/api/agent", tags=["Autonomous Course Agent"])


class StartAgentRequest(BaseModel):
    user_id: str = "default_student"
    course_id: str = settings.CANVAS_COURSE_ID
    dry_run: bool = True


@router.get("/status")
async def agent_status(user_id: str = "default_student", course_id: str = settings.CANVAS_COURSE_ID) -> Dict[str, Any]:
    return await get_autonomous_agent(user_id, course_id).get_run() or {
        "state": "idle", "user_id": user_id, "course_id": course_id
    }


@router.post("/start")
async def start_agent(req: StartAgentRequest) -> Dict[str, Any]:
    agent = get_autonomous_agent(req.user_id, req.course_id)
    return await agent.start(dry_run=req.dry_run)


@router.post("/pause")
async def pause_agent(user_id: str = "default_student", course_id: str = settings.CANVAS_COURSE_ID) -> Dict[str, Any]:
    return await get_autonomous_agent(user_id, course_id).pause()


@router.post("/resume")
async def resume_agent(user_id: str = "default_student", course_id: str = settings.CANVAS_COURSE_ID) -> Dict[str, Any]:
    return await get_autonomous_agent(user_id, course_id).resume()


@router.post("/stop")
async def stop_agent(user_id: str = "default_student", course_id: str = settings.CANVAS_COURSE_ID) -> Dict[str, Any]:
    return await get_autonomous_agent(user_id, course_id).stop()


@router.post("/discover")
async def discover_agent(user_id: str = "default_student", course_id: str = settings.CANVAS_COURSE_ID) -> Dict[str, Any]:
    agent = get_autonomous_agent(user_id, course_id)
    run = await agent.get_run()
    if not run:
        raise HTTPException(status_code=409, detail="Start an agent run before discovery.")
    return await agent.discover_and_plan(run["run_id"])
