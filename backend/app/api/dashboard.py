from fastapi import APIRouter
from app.db.mongodb import get_database

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get("/stats")
async def dashboard_stats():

    db = get_database()

    document_count = await db.documents.count_documents({})
    resume_count = await db.resume_analyses.count_documents({})

    return {
        "documents": document_count,
        "resumes": resume_count,
        "translations": 0,
        "chats": 0,
    }