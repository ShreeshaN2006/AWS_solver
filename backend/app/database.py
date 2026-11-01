from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import logging
from typing import Optional
from app.config import settings

logger = logging.getLogger("app.database")

class DatabaseManager:
    client: Optional[AsyncIOMotorClient] = None
    db: Optional[AsyncIOMotorDatabase] = None

    @classmethod
    async def connect(cls):
        try:
            logger.info(f"Connecting to MongoDB at {settings.MONGODB_URI}...")
            cls.client = AsyncIOMotorClient(settings.MONGODB_URI, serverSelectionTimeoutMS=5000, connectTimeoutMS=5000)
            cls.db = cls.client[settings.MONGODB_DB_NAME]
            await cls.client.admin.command('ping')
            logger.info(f"Connected successfully to MongoDB database: {settings.MONGODB_DB_NAME}")
            await cls.create_indexes()
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}. Will run in memory fallback if required.")

    @classmethod
    async def create_indexes(cls):
        if cls.db is None:
            return
        try:
            await cls.db.courses.create_index("course_id", unique=True)
            await cls.db.modules.create_index([("course_id", 1), ("module_id", 1)], unique=True)
            await cls.db.modules.create_index("order")
            await cls.db.module_items.create_index([("module_id", 1), ("item_id", 1)])
            await cls.db.learning_documents.create_index("doc_id", unique=True)
            await cls.db.learning_documents.create_index([("course_id", 1), ("module_id", 1)])
            await cls.db.document_chunks.create_index("chunk_id", unique=True)
            await cls.db.document_chunks.create_index([("course_id", 1), ("module_id", 1)])
            await cls.db.document_chunks.create_index("doc_id")
            await cls.db.chat_sessions.create_index("session_id", unique=True)
            await cls.db.chat_sessions.create_index([("user_id", 1), ("updated_at", -1)])
            await cls.db.chat_messages.create_index([("session_id", 1), ("created_at", 1)])
            await cls.db.practice_questions.create_index("question_id", unique=True)
            await cls.db.practice_questions.create_index([("module_id", 1), ("difficulty", 1)])
            await cls.db.practice_attempts.create_index([("user_id", 1), ("created_at", -1)])
            await cls.db.lab_progress.create_index([("user_id", 1), ("lab_id", 1)], unique=True)
            await cls.db.user_progress.create_index([("user_id", 1), ("course_id", 1), ("item_id", 1)], unique=True)
            await cls.db.study_plans.create_index([("user_id", 1), ("course_id", 1)])

            # Autonomous agent state: one current run per user/course, idempotent tasks,
            # immutable-ish discovery snapshots for recovery/audit.
            await cls.db.agent_runs.create_index([("user_id", 1), ("course_id", 1)], unique=True)
            await cls.db.agent_tasks.create_index([("user_id", 1), ("task_key", 1)], unique=True)
            await cls.db.agent_tasks.create_index([("run_id", 1), ("state", 1), ("priority", 1)])
            await cls.db.agent_discovery.create_index([("user_id", 1), ("course_id", 1)], unique=True)

            logger.info("MongoDB indexes verified.")
        except Exception as e:
            logger.warning(f"Error creating indexes: {e}")

    @classmethod
    async def close(cls):
        if cls.client:
            cls.client.close()
            logger.info("MongoDB connection closed.")

def get_database() -> AsyncIOMotorDatabase:
    if DatabaseManager.db is None:
        raise RuntimeError("Database connection has not been initialized.")
    return DatabaseManager.db
