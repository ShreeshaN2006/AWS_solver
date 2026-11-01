from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, date

class StudyTask(BaseModel):
    task_id: str
    title: str
    module_id: Optional[str] = None
    module_title: Optional[str] = None
    task_type: str  # "reading", "video", "lab", "practice_quiz", "revision"
    duration_mins: int
    is_completed: bool = False
    priority: str = "medium"  # "high", "medium", "low"
    reason: Optional[str] = None

class DailySchedule(BaseModel):
    day_number: int
    date: str  # YYYY-MM-DD
    focus_topic: str
    target_study_mins: int
    tasks: List[StudyTask] = []
    is_rest_day: bool = False

class StudyPlan(BaseModel):
    plan_id: str
    user_id: str = "default_student"
    course_id: str = "183194"
    target_completion_date: str
    weekly_hours_available: float = 7.0
    daily_available_mins: int = 60
    learning_pace: str = "balanced"  # "intensive", "balanced", "relaxed"
    schedules: List[DailySchedule] = []
    total_estimated_hours: float = 24.0
    focus_areas: List[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class GeneratePlanRequest(BaseModel):
    target_completion_date: Optional[str] = None
    weekly_hours: float = 7.0
    daily_study_mins: int = 60
    prioritize_weak_topics: bool = True
    include_all_labs: bool = True
