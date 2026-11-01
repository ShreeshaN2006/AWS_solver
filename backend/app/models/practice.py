from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class QuestionOption(BaseModel):
    id: str  # "A", "B", "C", "D"
    text: str

class PracticeQuestion(BaseModel):
    question_id: str
    module_id: str
    module_title: str
    question_type: str  # "multiple_choice", "true_false", "scenario", "conceptual", "difficult"
    difficulty: str = "medium"  # "easy", "medium", "hard"
    prompt: str
    scenario: Optional[str] = None
    options: List[QuestionOption]
    correct_option_id: str
    explanation: str
    concept_tags: List[str] = []
    aws_services: List[str] = []
    source_reference: Optional[str] = None

class AnswerSubmission(BaseModel):
    question_id: str
    selected_option_id: str

class QuestionResult(BaseModel):
    question_id: str
    prompt: str
    selected_option_id: str
    correct_option_id: str
    is_correct: bool
    explanation: str
    concept_tags: List[str]
    aws_services: List[str]

class PracticeSessionSubmission(BaseModel):
    module_id: Optional[str] = None  # None or "all" for mock exam
    is_comprehensive_exam: bool = False
    answers: List[AnswerSubmission]
    time_spent_seconds: int = 0

class PracticeAttempt(BaseModel):
    attempt_id: str
    user_id: str = "default_student"
    module_id: Optional[str] = None
    module_title: Optional[str] = None
    is_comprehensive_exam: bool = False
    total_questions: int
    correct_count: int
    score_percentage: float
    time_spent_seconds: int
    results: List[QuestionResult]
    weak_concepts: List[str] = []
    recommended_revision_topics: List[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
