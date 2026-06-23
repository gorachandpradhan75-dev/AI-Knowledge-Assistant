"""
Shared Pydantic schemas used across multiple modules.
"""
from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class APIResponse(BaseModel):
    success: bool = True
    message: str = "OK"
    data: Optional[Any] = None


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    error_code: Optional[str] = None


class PaginationParams(BaseModel):
    page: int = 1
    page_size: int = 20


class PaginatedResponse(BaseModel):
    success: bool = True
    page: int
    page_size: int
    total: int
    items: list[Any]


class TimestampedModel(BaseModel):
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)