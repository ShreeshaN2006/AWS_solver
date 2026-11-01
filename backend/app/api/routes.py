import httpx
from fastapi import APIRouter, File, Form, Header, HTTPException, UploadFile

from app.models.schemas import LabStepRequest, ProgressUpdate, StudyPlanRequest, TutorRequest, TutorResponse
from app.services.agent_tools import agent_tools
from app.services.canvas_parser import canvas_parser
from app.core.config import settings
from app.services.document_ingestion import DocumentIngestionService
from app.services.embeddings import EmbeddingProviderError
from app.services.llm_provider import LLMProviderError, get_llm_provider
from app.services.retrieval import retrieval_service

router = APIRouter()
ingestion = DocumentIngestionService()


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}


@router.get("/dashboard")
def dashboard() -> dict:
    return agent_tools.dashboard().model_dump()


@router.get("/course/outline")
def course_outline() -> dict:
    return agent_tools.get_course_outline()


@router.get("/modules/{module_id}")
def module_details(module_id: str) -> dict:
    module = agent_tools.get_module_details(module_id)
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    return module


@router.post("/tutor/ask", response_model=TutorResponse)
def tutor_ask(payload: TutorRequest) -> TutorResponse:
    try:
        explained = agent_tools.explain_topic(payload.question, module_id=payload.module_id)
        answer = get_llm_provider().respond(payload.question, explained["context"])
    except (LLMProviderError, EmbeddingProviderError) as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    return TutorResponse(answer=answer, sources=explained["sources"])


@router.get("/search")
def search(query: str, module_id: str | None = None) -> dict:
    try:
        return {"results": agent_tools.search_course_material(query, module_id=module_id)}
    except EmbeddingProviderError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@router.post("/canvas/parse")
async def canvas_parse(file: UploadFile = File(...)) -> dict:
    if not file.filename.endswith((".html", ".htm")):
        raise HTTPException(status_code=400, detail="Only HTML canvas exports are supported")
    content = (await file.read()).decode("utf-8", errors="ignore")
    items = canvas_parser.parse_modules(content)
    return {"items": [item.model_dump() for item in items]}


@router.get("/integrations/canvas/modules")
async def canvas_modules(authorization: str | None = Header(default=None)) -> dict:
    if not authorization:
        raise HTTPException(status_code=401, detail="Provide OAuth bearer token in Authorization header")
    headers = {"Authorization": authorization}
    url = f"{settings.canvas_base_url}/api/v1/courses/{settings.canvas_course_id}/modules"
    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return {"modules": response.json(), "mode": "read-only"}
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"Canvas API error: {exc}") from exc


@router.post("/documents/ingest")
async def ingest_document(
    module_id: str = Form(...),
    module_title: str = Form(...),
    document_name: str = Form(...),
    text: str = Form(...),
    learning_item_id: str | None = Form(default=None),
    source_url: str | None = Form(default=None),
) -> dict:
    try:
        chunks = ingestion.build_chunks(
            course_id=settings.canvas_course_id,
            module_id=module_id,
            module_title=module_title,
            document_name=document_name,
            text=text,
            learning_item_id=learning_item_id,
            source_url=source_url,
        )
        retrieval_service.ingest(chunks)
    except EmbeddingProviderError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    return {"ingested_chunks": len(chunks)}


@router.get("/practice/questions")
def practice_questions(module_id: str, difficulty: str = "medium") -> dict:
    questions = agent_tools.generate_practice_questions(module_id, difficulty)
    return {"questions": [question.model_dump(exclude={"answer"}) for question in questions]}


@router.post("/practice/evaluate")
def practice_evaluate(question_id: str = Form(...), selected_answer: str = Form(...)) -> dict:
    if question_id not in agent_tools.practice_questions:
        raise HTTPException(status_code=404, detail="Question not found")
    return agent_tools.evaluate_practice_answer(question_id, selected_answer).model_dump()


@router.get("/labs/{lab_id}")
def lab_details(lab_id: str) -> dict:
    return agent_tools.get_lab_instructions(lab_id)


@router.post("/labs/{lab_id}/guide")
def lab_guide(lab_id: str, payload: LabStepRequest) -> dict:
    return agent_tools.guide_lab_step(lab_id, payload.step)


@router.post("/progress/record")
def record_progress(payload: ProgressUpdate) -> dict:
    return agent_tools.record_learning_progress(payload.item_id, payload.module_id, payload.status)


@router.post("/study-plan")
def study_plan(payload: StudyPlanRequest) -> dict:
    return agent_tools.generate_study_plan(payload.available_time).model_dump()
