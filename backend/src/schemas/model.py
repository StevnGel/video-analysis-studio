from pydantic import BaseModel, Field
from typing import Optional, Literal, Dict, Any
from datetime import datetime


class ModelBase(BaseModel):
    """模型基础模型"""
    name: str = Field(..., description="模型名称")
    type: Literal["local", "external"] = Field(..., description="模型类型")
    status: Literal["active", "inactive"] = Field(default="inactive", description="模型状态")
    description: Optional[str] = Field(None, description="模型描述")
    config: Dict[str, Any] = Field(default_factory=dict, description="模型配置")


class ModelCreate(ModelBase):
    """创建模型模型"""
    pass


class ModelUpdate(BaseModel):
    """更新模型模型"""
    name: Optional[str] = Field(None, description="模型名称")
    status: Optional[Literal["active", "inactive"]] = Field(None, description="模型状态")
    description: Optional[str] = Field(None, description="模型描述")
    config: Optional[Dict[str, Any]] = Field(None, description="模型配置")


class Model(ModelBase):
    """模型响应模型"""
    id: str = Field(..., description="模型ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    
    class Config:
        from_attributes = True
