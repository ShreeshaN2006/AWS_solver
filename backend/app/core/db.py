from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings


class MongoConnection:
    def __init__(self) -> None:
        self.client: AsyncIOMotorClient | None = None

    async def connect(self) -> None:
        self.client = AsyncIOMotorClient(settings.mongodb_uri, serverSelectionTimeoutMS=3000)

    async def close(self) -> None:
        if self.client:
            self.client.close()


mongo = MongoConnection()
