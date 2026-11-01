import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.database import DatabaseManager
from app.seed_data.course_seed import seed_course_data
from app.seed_data.practice_seed import seed_practice_questions
from app.services.lab_service import lab_service

from app.api.courses import router as courses_router
from app.api.chat import router as chat_router
from app.api.practice import router as practice_router
from app.api.labs import router as labs_router
from app.api.progress import router as progress_router
from app.api.planner import router as planner_router
from app.api.documents import router as documents_router
from app.api.canvas import router as canvas_router
from app.api.settings import router as settings_router
from app.api.autonomous import router as autonomous_router

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("app.main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing AWS Academy Autonomous Course Agent Backend...")
    await DatabaseManager.connect()
    try:
        await seed_course_data()
        await seed_practice_questions()
        await lab_service.init_seed_labs()
        logger.info("Course modules, practice questions, and lab guides seeded successfully.")
    except Exception as e:
        logger.error(f"Error during initial seed: {e}")
    yield
    await DatabaseManager.close()
    logger.info("Shutdown completed.")

app = FastAPI(
    title="AWS Academy Autonomous Course Agent API",
    description="Autonomous, stateful course planning and execution service for AWS Academy Cloud Foundations (ID: 183194).",
    version="1.1.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(courses_router)
app.include_router(chat_router)
app.include_router(practice_router)
app.include_router(labs_router)
app.include_router(progress_router)
app.include_router(planner_router)
app.include_router(documents_router)
app.include_router(canvas_router)
app.include_router(settings_router)
app.include_router(autonomous_router)

@app.get("/api/health")
async def health_check():
    db_connected = False
    if DatabaseManager.client:
        try:
            await DatabaseManager.client.admin.command('ping')
            db_connected = True
        except Exception:
            db_connected = False
    return {
        "status": "healthy" if db_connected else "degraded",
        "service": "AWS Academy Autonomous Course Agent",
        "course_id": "183194",
        "mongodb_connected": db_connected,
        "active_llm_provider": settings.LLM_PROVIDER
    }

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global unhandled error at {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(status_code=500, content={"detail": "An internal server error occurred. Please verify logs or backend configuration."})
