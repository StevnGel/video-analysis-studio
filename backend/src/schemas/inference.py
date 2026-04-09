"""Inference schemas"""

from datetime import datetime
from enum import Enum
from typing import Any, List, Literal, Optional

from pydantic import BaseModel, Field


class InferenceStatus(str, Enum):
    """Inference status enumeration"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class InferenceConfig(BaseModel):
    """Inference configuration"""
    confidence_threshold: float = 0.25
    iou_threshold: float = 0.45
    max_det: int = 300
    classes: Optional[list[int]] = None
    device: str = "cpu"
    batch_size: int = 4
    half_precision: bool = False
    track_objects: bool = False


class DrawConfig(BaseModel):
    """Drawing configuration"""
    draw_bbox: bool = True
    draw_mask: bool = False
    draw_label: bool = True
    draw_confidence: bool = True
    bbox_color: str = "#00FF00"
    mask_alpha: float = 0.5
    line_thickness: int = 2
    font_scale: float = 0.8
    label_prefix: Optional[str] = None
    z_order: int = 0


class ModelItem(BaseModel):
    """Model item configuration"""
    name: str
    config: Optional[InferenceConfig] = None
    enabled: bool = True
    for_display: bool = True
    draw_config: Optional[DrawConfig] = None


class ModelConfig(BaseModel):
    """Model configuration"""
    parallel: bool = True
    models: List[ModelItem]


class InferenceCreate(BaseModel):
    """Inference creation request"""
    model_config: ModelConfig


class Detection(BaseModel):
    """Detection result"""
    class_id: int
    class_name: str
    confidence: float
    bbox: List[float]
    tracking_id: Optional[int] = None


class FrameResult(BaseModel):
    """Frame result"""
    frame_index: int
    timestamp: float
    detections: List[Detection]


class InferenceSummary(BaseModel):
    """Inference summary"""
    total_frames: int
    total_detections: int
    avg_fps: float


class InferenceResults(BaseModel):
    """Inference results"""
    frames: List[FrameResult]
    summary: InferenceSummary


class InferenceResponse(BaseModel):
    """Inference response"""
    inference_id: str
    task_id: str
    model_config: ModelConfig
    status: InferenceStatus = InferenceStatus.PENDING
    progress: float = 0.0
    results: Optional[InferenceResults] = None
    result_url: Optional[str] = None
    error_message: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None


class InferenceListResponse(BaseModel):
    """Inference list response"""
    inferences: List[InferenceResponse]


class InferenceStopResponse(BaseModel):
    """Inference stop response"""
    inference_id: str
    status: str