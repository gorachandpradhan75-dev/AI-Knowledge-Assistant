"""
Mongo document shapes for the `chats` collection.

Each chat document represents one conversation/session and embeds its
message history. This keeps reads for "load this conversation" to a
single document fetch, while `memory_service` can still summarize
across many chats per user for long-term personalization.
"""
from datetime import datetime, timezone
from typing import Literal, Optional, TypedDict


class ChatMessage(TypedDict):
    role: Literal["user", "assistant", "system"]
    content: str
    timestamp: datetime
    sources: Optional[list[dict]]  # populated for RAG / web-search answers


def new_chat_document(user_id: str, session_id: str, title: str = "New Conversation") -> dict:
    now = datetime.now(timezone.utc)
    return {
        "session_id": session_id,
        "user_id": user_id,
        "title": title,
        "messages": [],
        "document_id": None,  # set when chat is scoped to an uploaded PDF (RAG mode)
        "language": "en",
        "created_at": now,
        "updated_at": now,
    }


def make_message(role: str, content: str, sources: Optional[list[dict]] = None) -> dict:
    return {
        "role": role,
        "content": content,
        "timestamp": datetime.now(timezone.utc),
        "sources": sources or [],
    }


CHAT_SCHEMA_EXAMPLE = {
    "_id": "ObjectId",
    "session_id": "str (unique)",
    "user_id": "str (ref users._id)",
    "title": "str",
    "messages": "[{role, content, timestamp, sources[]}]",
    "document_id": "str | null (ref documents.document_id, for PDF-scoped chats)",
    "language": "str",
    "created_at": "datetime",
    "updated_at": "datetime",
}