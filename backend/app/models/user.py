"""
Mongo document shape for the `users` collection.

These are plain dataclass-like helpers used for documentation and
construction convenience — MongoDB itself stays schemaless, but having
one canonical shape avoids drift across services.
"""
from datetime import datetime, timezone
from typing import Optional


def new_user_document(
    username: str,
    email: str,
    hashed_password: str,
    full_name: Optional[str] = None,
    role: str = "user",
) -> dict:
    now = datetime.now(timezone.utc)
    return {
        "username": username,
        "email": email,
        "full_name": full_name,
        "hashed_password": hashed_password,
        "role": role,  # "user" | "admin"
        "is_active": True,
        "preferred_language": "en",
        "created_at": now,
        "updated_at": now,
        "last_login": None,
    }


# Reference schema (for documentation / Docs/API_DOCUMENTATION.md):
USER_SCHEMA_EXAMPLE = {
    "_id": "ObjectId",
    "username": "str (unique)",
    "email": "str (unique)",
    "full_name": "str | null",
    "hashed_password": "str (bcrypt)",
    "role": "user | admin",
    "is_active": "bool",
    "preferred_language": "str (ISO 639-1, default 'en')",
    "created_at": "datetime",
    "updated_at": "datetime",
    "last_login": "datetime | null",
}