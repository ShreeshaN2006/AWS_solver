from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class ModuleItem(BaseModel):
    item_id: str
    module_id: str
    title: str
    type: str = "Page"  # "Page", "File", "Quiz", "ExternalTool", "ExternalUrl"
    url: Optional[str] = None
    position: int = 1
    description: Optional[str] = None
    is_completed: bool = False
    time_estimate_mins: int = 15

class CourseModule(BaseModel):
    module_id: str
    course_id: str = "183194"
    module_number: int  # 1 to 10 for core modules, 0 for intro, 11+ for extra
    title: str
    description: Optional[str] = None
    is_core_module: bool = True
    order: int
    items: List[ModuleItem] = []
    progress_percentage: float = 0.0
    status: str = "Not Started"  # "Not Started", "In Progress", "Needs Revision", "Ready for Assessment", "Completed"
    has_lab: bool = False
    lab_id: Optional[str] = None
    key_aws_services: List[str] = []
    topics: List[str] = []

class Course(BaseModel):
    course_id: str = "183194"
    name: str = "AWS Academy Cloud Foundations"
    code: str = "ACF-183194"
    canvas_url: str = "https://awsacademy.instructure.com/courses/183194/modules"
    total_modules: int = 10
    modules: List[CourseModule] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
