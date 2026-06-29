from pathlib import Path
from uuid import uuid4
from datetime import datetime

from fastapi import APIRouter, UploadFile, File

from app.db.mongodb import get_database

from app.schemas.resume_schema import (
    ResumeAnalysisResponse,
)
from app.services.resume_service import (
    analyze_resume,
)

router = APIRouter(
    prefix="/resume",
    tags=["Resume Analyzer"]
)

UPLOAD_DIR = Path("storage/resumes")
UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)


@router.post(
    "/analyze",
    response_model=ResumeAnalysisResponse
)
async def analyze_resume_endpoint(
    file: UploadFile = File(...)
):

    resume_id = str(uuid4())

    file_path = (
        UPLOAD_DIR /
        f"{resume_id}_{file.filename}"
    )

    content = await file.read()

    with open(file_path, "wb") as f:
        f.write(content)

    result = await analyze_resume(
        str(file_path)
    )

    db = get_database()

    await db.resume_analyses.insert_one(
        {
            "resume_id": resume_id,
            "filename": file.filename,
            "score": result["score"],
            "skills": result["skills"],
            "education": result["education"],
            "experience": result["experience"],
            "suggestions": result["suggestions"],
            "created_at": datetime.utcnow(),
        }
    )

    return ResumeAnalysisResponse(
        filename=file.filename,
        score=result["score"],
        skills=result["skills"],
        education=result["education"],
        experience=result["experience"],
        suggestions=result["suggestions"],
    )