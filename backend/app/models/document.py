"""
Mongo document shape for the `documents` collection (uploaded PDFs).
"""
from datetime import datetime, timezone
from typing import Optional


def new_document_record(
    document_id: str,
    user_id: str,
    filename: str,
    file_path: str,
    page_count: int,
    char_count: int,
    summary: Optional[str] = None,
) -> dict:
    now = datetime.now(timezone.utc)
    return {
        "document_id": document_id,
        "user_id": user_id,
        "filename": filename,
        "file_path": file_path,
        "page_count": page_count,
        "char_count": char_count,
        "summary": summary,
        "faiss_index_path": None,
        "chunk_count": 0,
        "status": "processing",  # processing | ready | failed
        "uploaded_at": now,
        "updated_at": now,
    }


DOCUMENT_SCHEMA_EXAMPLE = {
    "_id": "ObjectId",
    "document_id": "str (unique)",
    "user_id": "str",
    "filename": "str",
    "file_path": "str",
    "page_count": "int",
    "char_count": "int",
    "summary": "str | null",
    "faiss_index_path": "str | null",
    "chunk_count": "int",
    "status": "processing | ready | failed",
    "uploaded_at": "datetime",
    "updated_at": "datetime",
}