from fastapi import APIRouter, HTTPException, Body
from typing import List, Dict, Any, Optional
from app.services.lab_service import lab_service
from app.models.lab import LabTroubleshootRequest, LabTroubleshootResponse

router = APIRouter(prefix="/api/labs", tags=["AWS Lab Assistant"])

@router.get("")
async def get_all_labs():
    """Retrieve all 6 AWS Academy Cloud Foundations labs."""
    return await lab_service.get_all_labs()

@router.get("/{lab_id}")
async def get_lab_by_id(lab_id: str):
    """Retrieve detailed instructions, objective, steps, and pitfalls for a specific lab."""
    lab = await lab_service.get_lab_by_id(lab_id)
    if not lab:
        raise HTTPException(status_code=404, detail=f"Lab {lab_id} not found.")
    return lab

@router.get("/{lab_id}/progress")
async def get_lab_user_progress(lab_id: str, user_id: str = "default_student"):
    """Get student progress and step confirmations for a lab."""
    return await lab_service.get_user_progress(user_id=user_id, lab_id=lab_id)

@router.post("/{lab_id}/steps/{step_number}/confirm")
async def confirm_lab_step(lab_id: str, step_number: int, confirmed: bool = Body(..., embed=True), user_id: str = "default_student"):
    """
    Allow student to confirm or unconfirm completion of a lab step.
    Adheres to safety rules: Never assume step success without student confirmation.
    """
    return await lab_service.update_step_progress(
        user_id=user_id,
        lab_id=lab_id,
        step_number=step_number,
        confirmed=confirmed
    )

@router.post("/troubleshoot", response_model=LabTroubleshootResponse)
async def troubleshoot_lab(req: LabTroubleshootRequest):
    """
    Troubleshoot AWS console errors or roadblocks submitted via error text or screenshot.
    Provides diagnostic explanation, verification steps, and safety reminders.
    """
    return await lab_service.troubleshoot(
        lab_id=req.lab_id,
        step_number=req.step_number,
        error_message=req.error_message,
        screenshot_base64=req.screenshot_base64,
        user_description=req.user_description
    )
