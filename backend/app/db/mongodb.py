"""
MongoDB connection lifecycle management using Motor (async driver).

`connect_to_mongo` / `close_mongo_connection` are wired into FastAPI's
startup/shutdown events in `app.main`. `get_database()` is the single
accessor used everywhere else in the codebase.
"""
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class MongoManager:
    client: AsyncIOMotorClient | None = None
    db: AsyncIOMotorDatabase | None = None


mongo_manager = MongoManager()


async def connect_to_mongo() -> None:
    logger.info(f"Connecting to MongoDB at {settings.MONGO_URI} ...")
    mongo_manager.client = AsyncIOMotorClient(settings.MONGO_URI, uuidRepresentation="standard")
    mongo_manager.db = mongo_manager.client[settings.MONGO_DB_NAME]
    # Fail fast if Mongo is unreachable
    await mongo_manager.client.admin.command("ping")
    logger.info("MongoDB connection established.")


async def close_mongo_connection() -> None:
    if mongo_manager.client:
        mongo_manager.client.close()
        logger.info("MongoDB connection closed.")


def get_database() -> AsyncIOMotorDatabase:
    if mongo_manager.db is None:
        raise RuntimeError("Database not initialized. Did the app startup event run?")
    return mongo_manager.db