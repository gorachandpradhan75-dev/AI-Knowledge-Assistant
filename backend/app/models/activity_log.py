"""
Mongo document shape for audit/activity logging.
"""
from datetime import datetime, timezone
from typing import Optional


def new_activity_log(
    user_id: str,
    action: str,
    details: Optional[dict] = None,
) -> dict:
    return {
        "user_id": user_id,
        "action": action,
        "details": details or {},
        "timestamp": datetime.now(timezone.utc),
    }


ACTIVITY_LOG_SCHEMA_EXAMPLE = {
    "_id": "ObjectId",
    "user_id": "str",
    "action": "str",
    "details": "dict",
    "timestamp": "datetime",
}