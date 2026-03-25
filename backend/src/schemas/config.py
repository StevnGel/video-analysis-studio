from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class ConfigBase(BaseModel):
    """配置基础模型"""
    key: str = Field(..., description="配置键")
    value: Dict[str, Any] = Field(..., description="配置值")
    description: Optional[str] = Field(None, description="配置描述")
    category: str = Field(default="system", description="配置分类")


class ConfigCreate(ConfigBase):
    """创建配置模型"""
    pass


class ConfigUpdate(BaseModel):
    """更新配置模型"""
    value: Optional[Dict[str, Any]] = Field(None, description="配置值")
    description: Optional[str] = Field(None, description="配置描述")
    category: Optional[str] = Field(None, description="配置分类")


class Config(ConfigBase):
    """配置响应模型"""
    id: str = Field(..., description="配置ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    
    class Config:
        from_attributes = True
