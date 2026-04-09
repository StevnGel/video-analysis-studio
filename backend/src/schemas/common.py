"""Common schemas"""

from typing import Any, Generic, List, Optional, TypeVar

from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    """Pagination parameters"""
    page: int = Field(default=1, ge=1, description="Page number")
    page_size: int = Field(default=20, ge=1, le=100, description="Items per page")


class PaginationMeta(BaseModel):
    """Pagination metadata"""
    page: int
    page_size: int
    total: int
    total_pages: int


T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """Standard API response"""
    code: int = Field(default=0, description="Response code (0 for success)")
    message: str = Field(default="success", description="Response message")
    data: Optional[T] = Field(default=None, description="Response data")
    request_id: Optional[str] = Field(default=None, description="Request tracking ID")


class ErrorDetail(BaseModel):
    """Error detail"""
    code: int = Field(description="Error code")
    message: str = Field(description="Error message")
    detail: Optional[dict] = Field(default=None, description="Detailed error info")


class VideoMetadata(BaseModel):
    """Video metadata"""
    bitrate: Optional[str] = None
    audio_codec: Optional[str] = None
    has_audio: Optional[bool] = None