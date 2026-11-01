from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime
from app.database import get_database
from app.models.practice import PracticeSessionSubmission, PracticeAttempt, QuestionResult
from app.services.agent import CourseCopilotTools

router = APIRouter(prefix="/api/practice", tags=["Knowledge Check & Practice"])

@router.get("/questions")
async def get_practice_questions(
    module_id: Optional[str] = Query(None, description="Module ID or omit for all"),
    difficulty: Optional[str] = Query(None, description="easy, medium, hard, or all"),
    question_type: Optional[str] = Query(None, description="multiple_choice, scenario, true_false, conceptual, difficult"),
    limit: int = Query(10, ge=1, le=50)
):
    """Retrieve practice questions filtered by module, difficulty, or question type."""
    db = get_database()
    filter_q: Dict[str, Any] = {}
    if module_id and module_id != "all":
        filter_q["module_id"] = str(module_id)
    if difficulty and difficulty != "all":
        filter_q["difficulty"] = difficulty
    if question_type and question_type != "all":
        filter_q["question_type"] = question_type

    questions = []
    # Project excluding correct_option_id from initial practice response if desired,
    # or include so client can evaluate locally or submit to server
    async for doc in db.practice_questions.find(filter_q, {"_id": 0}).limit(limit):
        questions.append(doc)
    return questions

@router.post("/submit", response_model=PracticeAttempt)
async def submit_practice_session(submission: PracticeSessionSubmission, user_id: str = "default_student"):
    """
    Evaluate practice quiz answers, calculate score percentage,
    isolate weak concepts, generate revision recommendations, and record attempt.
    """
    db = get_database()
    total_q = len(submission.answers)
    if total_q == 0:
        raise HTTPException(status_code=400, detail="No answers submitted.")

    correct_count = 0
    results: List[QuestionResult] = []
    weak_concepts = []
    recommended_topics = []

    for ans in submission.answers:
        q = await db.practice_questions.find_one({"question_id": ans.question_id}, {"_id": 0})
        if not q:
            continue
        
        is_correct = (q.get("correct_option_id") == ans.selected_option_id)
        if is_correct:
            correct_count += 1
        else:
            for tag in q.get("concept_tags", []):
                weak_concepts.append(tag)
            for s in q.get("aws_services", []):
                recommended_topics.append(f"Review {s} service characteristics")

        results.append(QuestionResult(
            question_id=ans.question_id,
            prompt=q.get("prompt", ""),
            selected_option_id=ans.selected_option_id,
            correct_option_id=q.get("correct_option_id", ""),
            is_correct=is_correct,
            explanation=q.get("explanation", ""),
            concept_tags=q.get("concept_tags", []),
            aws_services=q.get("aws_services", [])
        ))

    score_pct = round((correct_count / total_q) * 100, 1)
    unique_weak = list(set(weak_concepts))
    unique_recs = list(set(recommended_topics))
    if not unique_recs and score_pct < 80:
        unique_recs = ["Review AWS Shared Responsibility Model", "Inspect Cloud Foundations Student Guide"]

    attempt_id = f"att_{uuid.uuid4().hex[:10]}"
    attempt = PracticeAttempt(
        attempt_id=attempt_id,
        user_id=user_id,
        module_id=submission.module_id,
        module_title="Comprehensive Mock Exam" if submission.is_comprehensive_exam else f"Module {submission.module_id}",
        is_comprehensive_exam=submission.is_comprehensive_exam,
        total_questions=total_q,
        correct_count=correct_count,
        score_percentage=score_pct,
        time_spent_seconds=submission.time_spent_seconds,
        results=results,
        weak_concepts=unique_weak,
        recommended_revision_topics=unique_recs,
        created_at=datetime.utcnow()
    )

    await db.practice_attempts.insert_one(attempt.model_dump())
    return attempt

@router.get("/attempts")
async def list_user_attempts(user_id: str = "default_student"):
    """Retrieve history of student practice attempts and test scores."""
    db = get_database()
    attempts = []
    async for a in db.practice_attempts.find({"user_id": user_id}, {"_id": 0}).sort("created_at", -1):
        attempts.append(a)
    return attempts
