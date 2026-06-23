"""
Utility helpers for uploaded files.
"""
import re
from pathlib import Path
from uuid import uuid4


def safe_filename(filename: str) -> str:
    """
    Removes unsafe characters while preserving extension.
    """
    filename = Path(filename).name
    filename = re.sub(r"[^A-Za-z0-9._-]", "_", filename)
    return filename


def unique_filename(filename: str) -> str:
    """
    Generates a unique filename to avoid collisions.
    """
    safe_name = safe_filename(filename)
    ext = Path(safe_name).suffix
    stem = Path(safe_name).stem

    return f"{stem}_{uuid4().hex[:8]}{ext}"