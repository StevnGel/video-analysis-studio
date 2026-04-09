"""Model API routes"""

import logging
from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/models", tags=["models"])


@router.get("")
async def list_models():
    """Get available models list"""
    from ..services import get_model_service

    service = get_model_service()
    models = service.list_models()
    return {"models": models}


@router.get("/{model_name}")
async def get_model(model_name: str):
    """Get model details"""
    from ..services import get_model_service

    service = get_model_service()
    try:
        model = service.get_model(model_name)
        return model
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/instances")
async def get_instances():
    """Get model instances status"""
    from ..services import get_model_service

    service = get_model_service()
    try:
        instances = await service.get_instances()
        return {"instances": instances}
    except Exception as e:
        logger.error(f"Failed to get instances: {e}")
        return {"instances": []}