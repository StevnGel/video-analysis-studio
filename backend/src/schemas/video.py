"""Video source schemas"""

from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, Field

from .common import PaginationMeta, VideoMetadata


class VideoSource(BaseModel):
    """Video source data model"""
    id: str = Field(description="Video source unique identifier")
    name: str = Field(description="Video display name")
    original_name: str = Field(description="Original file name")
    type: Literal["file", "rtsp"] = Field(description="Video source type")
    path: str = Field(description="File path or RTSP address")
    size: int = Field(description="File size in bytes")
    duration: float = Field(description="Video duration in seconds")
    width: int = Field(description="Video width")
    height: int = Field(description="Video height")
    fps: float = Field(description="Frame rate")
    codec: str = Field(description="Video codec")
    status: Literal["ready", "processing", "deleted"] = Field(default="ready", description="Status")
    tags: Optional[List[str]] = Field(default=None, description="Video tags")
    metadata: Optional[VideoMetadata] = Field(default=None, description="Additional metadata")
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Update timestamp")


class VideoUploadResponse(BaseModel):
    """Video upload response"""
    id: str
    name: str
    original_name: str
    type: Literal["file", "rtsp"]
    path: str
    size: int
    duration: float
    width: int
    height: int
    fps: float
    codec: str
    status: str
    tags: Optional[List[str]] = None
    created_at: datetime
    updated_at: datetime


class VideoListResponse(BaseModel):
    """Video list response"""
    videos: List[VideoSource]
    pagination: PaginationMeta


class VideoSourceInput(BaseModel):
    """Video source input configuration"""
    type: Literal["local", "rtsp", "http", "https"] = Field(description="Video source type")
    id: Optional[str] = Field(default=None, description="Local video source ID")
    url: Optional[str] = Field(default=None, description="Online video address")
    auto_download: bool = Field(default=True, description="Auto download to local")
    timeout: int = Field(default=300, description="Download timeout in seconds")


class VideoDeleteResponse(BaseModel):
    """Video delete response"""
    deleted_id: str