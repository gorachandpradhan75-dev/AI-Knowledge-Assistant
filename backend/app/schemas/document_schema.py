"""
Document upload / PDF processing schemas.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class DocumentUploadResponse(BaseModel):
    document_id: str
    filename: str
    page_count: int
    char_count: int
    chunk_count: int
    status: str


class SummarizeResponse(BaseModel):
    document_id: str
    summary: str


class DocumentQuestionRequest(BaseModel):
    question: str
    language: str = "en"


class DocumentQuestionResponse(BaseModel):
    answer: str
    sources: list[dict] = []


class DocumentInfoResponse(BaseModel):
    document_id: str
    filename: str
    page_count: int
    char_count: int
    chunk_count: int
    status: str
    uploaded_at: datetime
    summary: Optional[str] = None
class SummaryRequest(BaseModel):
    language: str = "en"
    length: str = "medium"