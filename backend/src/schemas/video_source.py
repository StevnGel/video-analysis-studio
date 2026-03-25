from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime


class VideoSourceBase(BaseModel):
    """视频源基础模型"""
    name: str = Field(..., description="视频源名称")
    type: Literal["file", "stream"] = Field(..., description="视频源类型")
    url: str = Field(..., description="视频源URL")
    status: Literal["active", "inactive"] = Field(default="inactive", description="视频源状态")
    description: Optional[str] = Field(None, description="视频源描述")
    resolution: Optional[str] = Field(None, description="分辨率")
    framerate: Optional[int] = Field(None, description="帧率")


class VideoSourceCreate(VideoSourceBase):
    """创建视频源模型"""
    pass


class VideoSourceUpdate(BaseModel):
    """更新视频源模型"""
    name: Optional[str] = Field(None, description="视频源名称")
    status: Optional[Literal["active", "inactive"]] = Field(None, description="视频源状态")
    description: Optional[str] = Field(None, description="视频源描述")
    resolution: Optional[str] = Field(None, description="分辨率")
    framerate: Optional[int] = Field(None, description="帧率")


class VideoSource(VideoSourceBase):
    """视频源响应模型"""
    id: str = Field(..., description="视频源ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    
    class Config:
        from_attributes = True
