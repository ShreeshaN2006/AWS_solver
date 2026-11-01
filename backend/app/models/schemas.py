from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class ProgressState(str, Enum):
    not_started = "Not Started"
    in_progress = "In Progress"
    needs_revision = "Needs Revision"
    ready_for_assessment = "Ready for Assessment"
    completed = "Completed"


class Module(BaseModel):
    module_id: str
    module_number: int
    title: str
    progress_percentage: float = 0
    resources: list[str] = Field(default_factory=list)
    has_lab: bool = False
    status: ProgressState = ProgressState.not_started


class DashboardStats(BaseModel):
    course_title: str
    total_modules: int
    completed_modules: int
    modules_in_progress: int
    remaining_modules: int
    overall_study_progress: float
    recent_learning_activity: list[str]
    upcoming_tasks: list[str]
    weak_topics: list[str]
    recommended_next_activity: str


class DocumentChunk(BaseModel):
    course_id: int
    module_id: str
    module_title: str
    learning_item_id: str | None = None
    document_name: str
    page_number: int | None = None
    timestamp: str | None = None
    extracted_content: str
    embedding: list[float]
    source_url: str | None = None


class TutorRequest(BaseModel):
    question: str
    module_id: str | None = None
    session_id: str | None = None


class TutorResponse(BaseModel):
    answer: str
    sources: list[dict[str, Any]]


class PracticeQuestionType(str, Enum):
    mcq = "multiple_choice"
    true_false = "true_false"
    scenario = "scenario"
    conceptual = "conceptual"


class PracticeQuestion(BaseModel):
    question_id: str
    module_id: str
    difficulty: str
    qtype: PracticeQuestionType
    prompt: str
    options: list[str] = Field(default_factory=list)
    answer: str
    explanation: str


class PracticeSubmission(BaseModel):
    question_id: str
    selected_answer: str


class PracticeEvaluation(BaseModel):
    is_correct: bool
    correct_answer: str
    explanation: str


class ProgressUpdate(BaseModel):
    item_id: str
    module_id: str
    status: ProgressState
    notes: str | None = None


class StudyPlanRequest(BaseModel):
    available_time: str


class StudyPlan(BaseModel):
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    schedule: list[dict[str, str]]


class LabStepRequest(BaseModel):
    step: int


class CourseOutlineItem(BaseModel):
    module_id: str
    module_title: str
    item_title: str
    item_link: str | None = None
