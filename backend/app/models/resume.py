"""
Mongo document shape for resume analysis results.
"""
from datetime import datetime, timezone


def new_resume_analysis(
    analysis_id: str,
    user_id: str,
    filename: str,
    extracted_text: str,
    analysis_result: dict,
) -> dict:
    now = datetime.now(timezone.utc)
    return {
        "analysis_id": analysis_id,
        "user_id": user_id,
        "filename": filename,
        "extracted_text": extracted_text,
        "analysis_result": analysis_result,
        "analyzed_at": now,
    }


RESUME_ANALYSIS_SCHEMA_EXAMPLE = {
    "_id": "ObjectId",
    "analysis_id": "str",
    "user_id": "str",
    "filename": "str",
    "extracted_text": "str",
    "analysis_result": "dict",
    "analyzed_at": "datetime",
}