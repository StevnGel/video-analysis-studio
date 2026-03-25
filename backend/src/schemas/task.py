from pydantic import BaseModel, Field
from typing import Optional, Literal, Dict, Any
from datetime import datetime


class TaskBase(BaseModel):
    """任务基础模型"""
    name: str = Field(..., description="任务名称")
    video_source_id: str = Field(..., description="视频源ID")
    model_id: str = Field(..., description="模型ID")
    status: Literal["pending", "running", "paused", "completed", "failed"] = Field(default="pending", description="任务状态")
    description: Optional[str] = Field(None, description="任务描述")
    config: Dict[str, Any] = Field(default_factory=dict, description="任务配置")


class TaskCreate(TaskBase):
    """创建任务模型"""
    pass


class TaskUpdate(BaseModel):
    """更新任务模型"""
    name: Optional[str] = Field(None, description="任务名称")
    status: Optional[Literal["pending", "running", "paused", "completed", "failed"]] = Field(None, description="任务状态")
    description: Optional[str] = Field(None, description="任务描述")
    config: Optional[Dict[str, Any]] = Field(None, description="任务配置")


class Task(TaskBase):
    """任务响应模型"""
    id: str = Field(..., description="任务ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    started_at: Optional[datetime] = Field(None, description="开始时间")
    completed_at: Optional[datetime] = Field(None, description="完成时间")
    
    class Config:
        from_attributes = True
