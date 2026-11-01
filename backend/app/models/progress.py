from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class TopicMastery(BaseModel):
    topic: str
    module_id: str
    status: str = "needs_study"  # "understood", "needs_revision", "needs_study"
    last_reviewed: Optional[datetime] = None
    quiz_score: Optional[float] = None

class ItemProgress(BaseModel):
    item_id: str
    module_id: str
    locally_completed: bool = False
    canvas_completed: Optional[bool] = None
    completed_at: Optional[datetime] = None
    time_spent_mins: int = 0

class UserModuleProgress(BaseModel):
    module_id: str
    module_number: int
    title: str
    status: str = "Not Started"  # "Not Started", "In Progress", "Needs Revision", "Ready for Assessment", "Completed"
    progress_percentage: float = 0.0
    items_completed: int = 0
    total_items: int = 0
    lab_completed: bool = False
    practice_best_score: Optional[float] = None
    last_activity_at: Optional[datetime] = None

class UserOverallProgress(BaseModel):
    user_id: str = "default_student"
    course_id: str = "183194"
    total_study_time_mins: int = 0
    overall_progress_percentage: float = 0.0
    total_modules: int = 10
    completed_modules: int = 0
    in_progress_modules: int = 0
    remaining_modules: int = 10
    modules_progress: List[UserModuleProgress] = []
    understood_topics: List[str] = []
    weak_topics: List[str] = []
    recent_activities: List[Dict[str, Any]] = []
    upcoming_tasks: List[Dict[str, Any]] = []
    recommended_next_activity: Optional[Dict[str, Any]] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)
