from pydantic import BaseModel, Field
from typing import Optional, Literal, Dict, Any
from datetime import datetime


class EventBase(BaseModel):
    """事件基础模型"""
    task_id: str = Field(..., description="任务ID")
    type: str = Field(..., description="事件类型")
    severity: Literal["low", "medium", "high", "critical"] = Field(default="medium", description="事件严重程度")
    status: Literal["new", "processed", "ignored"] = Field(default="new", description="事件状态")
    description: Optional[str] = Field(None, description="事件描述")
    data: Dict[str, Any] = Field(default_factory=dict, description="事件数据")


class EventCreate(EventBase):
    """创建事件模型"""
    pass


class EventUpdate(BaseModel):
    """更新事件模型"""
    status: Optional[Literal["new", "processed", "ignored"]] = Field(None, description="事件状态")
    description: Optional[str] = Field(None, description="事件描述")
    data: Optional[Dict[str, Any]] = Field(None, description="事件数据")


class Event(EventBase):
    """事件响应模型"""
    id: str = Field(..., description="事件ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    
    class Config:
        from_attributes = True
