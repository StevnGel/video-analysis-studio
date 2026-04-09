"""Models module - abstract model classes"""

from .base import VideoModel, ModelInput, ModelOutput, DetectionResult
from .yolo import YOLOModel
from .manager import ModelManager, ModelInstance, ModelInstancePool

__all__ = [
    "VideoModel",
    "ModelInput",
    "ModelOutput",
    "DetectionResult",
    "YOLOModel",
    "ModelManager",
    "ModelInstance",
    "ModelInstancePool",
]