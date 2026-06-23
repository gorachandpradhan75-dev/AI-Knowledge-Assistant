from pathlib import Path
import os
from uuid import uuid4
from datetime import datetime
from fastapi import APIRouter, UploadFile, File, HTTPException

from app.db.mongodb import get_database
from app.schemas.document_schema import (
    DocumentUploadResponse,
    DocumentQuestionRequest,
    DocumentQuestionResponse,
    SummarizeResponse,
    DocumentInfoResponse,
    SummaryRequest,
)
from app.services.pdf_service import (
    ingest_document,
    answer_question_from_document,
    generate_document_summary,
)

router = APIRouter(prefix="/documents", tags=["Documents"])

UPLOAD_DIR = Path("storage/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    document_id = str(uuid4())

    file_path = UPLOAD_DIR / f"{document_id}_{file.filename}"

    content = await file.read()

    with open(file_path, "wb") as f:
        f.write(content)

    metadata = await ingest_document(
        document_id=document_id,
        file_path=file_path,
    )

    db = get_database()

    await db.documents.insert_one(
    {
        "document_id": document_id,
        "filename": file.filename,
        "file_path": str(file_path),
        "page_count": metadata["page_count"],
        "char_count": metadata["char_count"],
        "chunk_count": metadata["chunk_count"],
        "status": "processed",
        "uploaded_at": datetime.utcnow(),
    }
)

    return DocumentUploadResponse(
        document_id=document_id,
        filename=file.filename,
        page_count=metadata["page_count"],
        char_count=metadata["char_count"],
        chunk_count=metadata["chunk_count"],
        status="processed",
    )


@router.post("/{document_id}/ask", response_model=DocumentQuestionResponse)
async def ask_document_question(
    document_id: str,
    request: DocumentQuestionRequest,
):
    result = await answer_question_from_document(
        document_id=document_id,
        question=request.question,
    )

    return DocumentQuestionResponse(
        answer=result["answer"],
        sources=result["sources"],
    )

@router.post(
    "/{document_id}/summary",
    response_model=SummarizeResponse,
)
async def summarize_document(
    document_id: str,
    request: SummaryRequest,
):

    summary = await generate_document_summary(
    document_id=document_id,
    length=request.length,
)

    return SummarizeResponse(
        document_id=document_id,
        summary=summary,
    )

@router.get(
    "",
    response_model=list[DocumentInfoResponse]
)
async def list_documents():

    db = get_database()

    documents = await db.documents.find().to_list(None)

    return [
        DocumentInfoResponse(
            document_id=doc["document_id"],
            filename=doc["filename"],
            page_count=doc.get("page_count", 0),
            char_count=doc.get("char_count", 0),
            chunk_count=doc.get("chunk_count", 0),
            status=doc.get("status", "unknown"),
            uploaded_at=doc.get("uploaded_at"),
            summary=doc.get("summary"),
        )
        for doc in documents
    ]

@router.get(
    "/{document_id}",
    response_model=DocumentInfoResponse,
)
async def get_document_details(
    document_id: str,
):

    db = get_database()

    document = await db.documents.find_one(
        {"document_id": document_id}
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )

    return DocumentInfoResponse(
        document_id=document["document_id"],
        filename=document["filename"],
        page_count=document.get("page_count", 0),
        char_count=document.get("char_count", 0),
        chunk_count=document.get("chunk_count", 0),
        status=document.get("status", "unknown"),
        uploaded_at=document.get("uploaded_at"),
        summary=document.get("summary"),
    )

@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
):

    db = get_database()

    document = await db.documents.find_one(
        {"document_id": document_id}
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )

    file_path = document.get("file_path")

    if file_path and os.path.exists(file_path):
        os.remove(file_path)

    await db.documents.delete_one(
        {"document_id": document_id}
    )

    return {
        "message": "Document deleted successfully"
    }