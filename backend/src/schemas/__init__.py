"""Data schemas module"""

from .video import VideoSource, VideoUploadResponse, VideoListResponse
from .task import TaskCreate, TaskResponse, TaskListResponse
from .inference import InferenceCreate, InferenceResponse, InferenceListResponse
from .common import PaginationParams, ApiResponse, ErrorDetail

__all__ = [
    "VideoSource",
    "VideoUploadResponse",
    "VideoListResponse",
    "TaskCreate",
    "TaskResponse",
    "TaskListResponse",
    "InferenceCreate",
    "InferenceResponse",
    "InferenceListResponse",
    "PaginationParams",
    "ApiResponse",
    "ErrorDetail",
]