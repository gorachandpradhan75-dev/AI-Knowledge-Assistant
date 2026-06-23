"""
Chat request/response schemas.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ChatMessageRequest(BaseModel):
    message: str = Field(..., min_length=1)
    session_id: Optional[str] = None
    document_id: Optional[str] = None
    language: str = "en"


class ChatMessageResponse(BaseModel):
    session_id: str
    answer: str
    sources: list[dict] = []


class ChatHistoryItem(BaseModel):
    role: str
    content: str
    timestamp: datetime
    sources: list[dict] = []


class ChatSessionResponse(BaseModel):
    session_id: str
    title: str
    document_id: Optional[str] = None
    language: str
    created_at: datetime
    updated_at: datetime


class ChatHistoryResponse(BaseModel):
    session_id: str
    messages: list[ChatHistoryItem]