from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class LabStep(BaseModel):
    step_number: int
    title: str
    objective: str
    console_navigation: str
    instructions: List[str]
    expected_result: str
    common_pitfalls: List[str] = []
    verification_check: str

class LabDetail(BaseModel):
    lab_id: str
    lab_number: int
    title: str
    duration_mins: int
    module_id: str
    module_title: str
    objective: str
    aws_services: List[str]
    architecture_summary: str
    steps: List[LabStep]
    final_summary: str
    canvas_item_id: Optional[str] = None

class LabStepProgress(BaseModel):
    step_number: int
    is_confirmed: bool = False
    confirmed_at: Optional[datetime] = None
    notes: Optional[str] = None

class UserLabProgress(BaseModel):
    user_id: str = "default_student"
    lab_id: str
    current_step: int = 1
    total_steps: int = 5
    completed_steps: List[int] = []
    is_completed: bool = False
    started_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    troubleshoot_history: List[Dict[str, Any]] = []

class LabTroubleshootRequest(BaseModel):
    lab_id: str
    step_number: int
    error_message: Optional[str] = None
    screenshot_base64: Optional[str] = None
    user_description: str

class LabTroubleshootResponse(BaseModel):
    lab_id: str
    step_number: int
    diagnosis: str
    suggested_fix: List[str]
    console_steps_to_verify: List[str]
    safety_reminder: str = "Note: Lab resources are simulated for guidance. Always verify within your AWS Academy Learner Lab Sandbox."
