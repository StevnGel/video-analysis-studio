"""Task schemas"""

from datetime import datetime
from enum import Enum
from typing import Any, List, Literal, Optional

from pydantic import BaseModel, Field

from .common import PaginationMeta


class TaskType(str, Enum):
    """Task type enumeration"""
    REALTIME = "realtime"
    OFFLINE = "offline"


class TaskStatus(str, Enum):
    """Task status enumeration"""
    PENDING = "pending"
    PENDING_WITH_INFERENCE = "pending_with_inference"
    QUEUED = "queued"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class VideoSourceInput(BaseModel):
    """Input video source configuration"""
    type: Literal["local", "rtsp", "http", "https"]
    id: Optional[str] = None
    url: Optional[str] = None
    auto_download: bool = True
    timeout: int = 300


class ResizeConfig(BaseModel):
    """Resize configuration"""
    width: int
    height: int
    maintain_aspect: bool = True


class ROIConfig(BaseModel):
    """ROI region configuration"""
    x1: int = 0
    y1: int = 0
    x2: int = -1
    y2: int = -1


class InputConfig(BaseModel):
    """Input configuration"""
    source: VideoSourceInput
    resize: Optional[ResizeConfig] = None
    roi: Optional[ROIConfig] = None
    skip_frames: int = 0
    buffer_size: int = 30
    decode_threads: int = 4


class OutputFormatConfig(BaseModel):
    """Output video format configuration"""
    width: Optional[int] = None
    height: Optional[int] = None
    fps: Optional[float] = None
    codec: Literal["h264", "h265"] = "h264"
    bitrate: str = "4M"
    gop_size: int = 30
    profile: str = "main"


class OutputConfig(BaseModel):
    """Output configuration"""
    type: Literal["file", "rtmp", "hls"] = "file"
    path: Optional[str] = None
    rtmp_url: Optional[str] = None
    hls_dir: Optional[str] = None
    format: Optional[OutputFormatConfig] = None


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
    """Drawing configuration for detections"""
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


class TaskStatistics(BaseModel):
    """Task statistics"""
    frames_processed: int = 0
    frames_total: int = 0
    detections_count: int = 0
    avg_fps: float = 0.0


class TaskCreate(BaseModel):
    """Task creation request"""
    name: str
    task_type: TaskType = TaskType.OFFLINE
    input_config: InputConfig
    output_config: OutputConfig
    model_settings: Optional[ModelConfig] = None
    priority: int = Field(default=50, ge=0, le=100)


class TaskResponse(BaseModel):
    """Task response"""
    id: str
    name: str
    task_type: str
    video_source_id: Optional[str] = None
    input_config: Optional[InputConfig] = None
    output_config: Optional[OutputConfig] = None
    model_settings: Optional[ModelConfig] = None
    status: TaskStatus = TaskStatus.PENDING
    progress: float = 0.0
    gpu_device: Optional[str] = None
    result_url: Optional[str] = None
    priority: int = 50
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    statistics: Optional[TaskStatistics] = None


class TaskListResponse(BaseModel):
    """Task list response"""
    tasks: List[TaskResponse]
    pagination: PaginationMeta


class TaskStartResponse(BaseModel):
    """Task start response"""
    task_id: str
    status: str
    started_at: datetime


class TaskStopResponse(BaseModel):
    """Task stop response"""
    task_id: str
    status: str


class TaskOutputResponse(BaseModel):
    """Task output response"""
    output_url: str
    output_type: str