from app.core.logging_config import logger
from app.db.mongodb import get_database


async def init_indexes() -> None:
    db = get_database()

    await db.users.create_index("email", unique=True)
    await db.users.create_index("username", unique=True)

    await db.chats.create_index([("user_id", 1), ("updated_at", -1)])
    await db.chats.create_index("session_id", unique=True)

    await db.documents.create_index([("user_id", 1), ("uploaded_at", -1)])
    await db.documents.create_index("document_id", unique=True)

    await db.embeddings.create_index("document_id")
    await db.embeddings.create_index(
        [("document_id", 1), ("chunk_index", 1)],
        unique=True,
    )

    await db.resume_analysis.create_index(
        [("user_id", 1), ("analyzed_at", -1)]
    )

    await db.activity_logs.create_index(
        [("user_id", 1), ("timestamp", -1)]
    )
    await db.activity_logs.create_index("action")

    logger.info("MongoDB indexes verified/created.")