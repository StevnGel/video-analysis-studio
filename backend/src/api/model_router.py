from typing import List
from fastapi import APIRouter, HTTPException, Depends
from src.schemas.model import Model, ModelCreate, ModelUpdate
from src.services.model_service import model_service

router = APIRouter(
    prefix="/api/models",
    tags=["models"],
    responses={404: {"description": "Not found"}},
)


@router.post("", response_model=Model)
def create_model(model: ModelCreate):
    """创建模型"""
    try:
        return model_service.create_model(model)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{model_id}", response_model=Model)
def get_model(model_id: str):
    """获取模型"""
    model = model_service.get_model(model_id)
    if not model:
        raise HTTPException(status_code=404, detail="模型不存在")
    return model


@router.get("", response_model=List[Model])
def get_models(limit: int = 100, offset: int = 0):
    """获取模型列表"""
    return model_service.get_models(limit, offset)


@router.put("/{model_id}", response_model=Model)
def update_model(model_id: str, model: ModelUpdate):
    """更新模型"""
    updated_model = model_service.update_model(model_id, model)
    if not updated_model:
        raise HTTPException(status_code=404, detail="模型不存在")
    return updated_model


@router.delete("/{model_id}")
def delete_model(model_id: str):
    """删除模型"""
    success = model_service.delete_model(model_id)
    if not success:
        raise HTTPException(status_code=404, detail="模型不存在")
    return {"message": "模型删除成功"}
