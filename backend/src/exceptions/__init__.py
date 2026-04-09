"""Custom exceptions module"""

from typing import Any, Optional


class VideoAnalysisError(Exception):
    """Base exception for video analysis studio"""
    def __init__(self, message: str, code: int = 9999):
        self.message = message
        self.code = code
        super().__init__(self.message)


class VideoNotFoundError(VideoAnalysisError):
    """Video not found exception"""
    def __init__(self, video_id: str):
        super().__init__(f"Video not found: {video_id}", code=1001)


class VideoUploadError(VideoAnalysisError):
    """Video upload error"""
    def __init__(self, message: str):
        super().__init__(message, code=1002)


class VideoFormatError(VideoAnalysisError):
    """Unsupported video format"""
    def __init__(self, format: str):
        super().__init__(f"Unsupported video format: {format}", code=1004)


class VideoSizeError(VideoAnalysisError):
    """Video file size exceeded"""
    def __init__(self, size: int, max_size: int):
        super().__init__(f"Video size {size} exceeds max {max_size}", code=1005)


class TaskNotFoundError(VideoAnalysisError):
    """Task not found exception"""
    def __init__(self, task_id: str):
        super().__init__(f"Task not found: {task_id}", code=2001)


class TaskCreateError(VideoAnalysisError):
    """Task creation error"""
    def __init__(self, message: str):
        super().__init__(message, code=2002)


class TaskStartError(VideoAnalysisError):
    """Task start error"""
    def __init__(self, message: str):
        super().__init__(message, code=2003)


class TaskStopError(VideoAnalysisError):
    """Task stop error"""
    def __init__(self, message: str):
        super().__init__(message, code=2004)


class ModelNotFoundError(VideoAnalysisError):
    """Model not found exception"""
    def __init__(self, model_name: str):
        super().__init__(f"Model not found: {model_name}", code=3001)


class ModelLoadError(VideoAnalysisError):
    """Model load error"""
    def __init__(self, model_name: str, message: str):
        super().__init__(f"Failed to load model {model_name}: {message}", code=3002)


class ModelInstanceError(VideoAnalysisError):
    """Model instance unavailable"""
    def __init__(self, message: str = "Model instance unavailable"):
        super().__init__(message, code=3003)


class InferenceNotFoundError(VideoAnalysisError):
    """Inference not found exception"""
    def __init__(self, inference_id: str):
        super().__init__(f"Inference not found: {inference_id}", code=4003)


class InferenceError(VideoAnalysisError):
    """Inference execution error"""
    def __init__(self, message: str):
        super().__init__(message, code=4001)


class GPUUnavailableError(VideoAnalysisError):
    """GPU resource unavailable"""
    def __init__(self, message: str = "GPU resource unavailable"):
        super().__init__(message, code=5001)


class GPUMemoryError(VideoAnalysisError):
    """GPU memory exhausted"""
    def __init__(self, message: str = "GPU memory exhausted"):
        super().__init__(message, code=5002)