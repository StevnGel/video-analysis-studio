from typing import List
from fastapi import APIRouter, HTTPException, Depends
from src.schemas.config import Config, ConfigCreate, ConfigUpdate
from src.services.config_service import config_service

router = APIRouter(
    prefix="/api/configs",
    tags=["configs"],
    responses={404: {"description": "Not found"}},
)


@router.post("", response_model=Config)
def create_config(config: ConfigCreate):
    """创建配置"""
    try:
        return config_service.create_config(config)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{config_id}", response_model=Config)
def get_config(config_id: str):
    """获取配置"""
    config = config_service.get_config(config_id)
    if not config:
        raise HTTPException(status_code=404, detail="配置不存在")
    return config


@router.get("/key/{key}", response_model=Config)
def get_config_by_key(key: str):
    """根据键获取配置"""
    config = config_service.get_config_by_key(key)
    if not config:
        raise HTTPException(status_code=404, detail="配置不存在")
    return config


@router.get("", response_model=List[Config])
def get_configs(limit: int = 100, offset: int = 0):
    """获取配置列表"""
    return config_service.get_configs(limit, offset)


@router.get("/category/{category}", response_model=List[Config])
def get_configs_by_category(category: str, limit: int = 100, offset: int = 0):
    """根据分类获取配置列表"""
    return config_service.get_configs_by_category(category, limit, offset)


@router.put("/{config_id}", response_model=Config)
def update_config(config_id: str, config: ConfigUpdate):
    """更新配置"""
    updated_config = config_service.update_config(config_id, config)
    if not updated_config:
        raise HTTPException(status_code=404, detail="配置不存在")
    return updated_config


@router.put("/key/{key}", response_model=Config)
def update_config_by_key(key: str, config: ConfigUpdate):
    """根据键更新配置"""
    updated_config = config_service.update_config_by_key(key, config)
    if not updated_config:
        raise HTTPException(status_code=404, detail="配置不存在")
    return updated_config


@router.delete("/{config_id}")
def delete_config(config_id: str):
    """删除配置"""
    success = config_service.delete_config(config_id)
    if not success:
        raise HTTPException(status_code=404, detail="配置不存在")
    return {"message": "配置删除成功"}
