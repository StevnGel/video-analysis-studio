"""Model manager with instance pool"""

import asyncio
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4

from pydantic import BaseModel

from .base import VideoModel

logger = logging.getLogger(__name__)


class ModelInstance(BaseModel):
    """Model instance"""
    instance_id: str
    model_name: str
    model_type: str
    device: str
    process_id: Optional[int] = None
    status: str = "loading"
    load_time: Optional[datetime] = None
    last_used: Optional[datetime] = None
    gpu_memory: int = 0


class ModelInstancePool:
    """Model instance pool for managing model instances"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self._instances: Dict[str, ModelInstance] = {}
        self._available_queue: asyncio.Queue = asyncio.Queue()
        self._models: Dict[str, VideoModel] = {}
        self._lock = asyncio.Lock()

    async def initialize(self) -> None:
        """Initialize instance pool"""
        gpu_instances = self.config.get("gpu_instances", [])
        logger.info(f"Initializing model instance pool with {len(gpu_instances)} GPU configs")

        for gpu_config in gpu_instances:
            device = gpu_config.get("device", "cpu")
            instance_count = gpu_config.get("instance_count", 1)
            model_name = gpu_config.get("model", "yolo_v8")

            for i in range(instance_count):
                instance_id = f"{model_name}-{device}-{i}-{uuid4().hex[:4]}"
                instance = ModelInstance(
                    instance_id=instance_id,
                    model_name=model_name,
                    model_type=model_name,
                    device=device,
                    status="ready",
                    load_time=datetime.now()
                )
                self._instances[instance_id] = instance
                await self._available_queue.put(instance_id)
                logger.info(f"Created model instance {instance_id}")

    async def acquire(self, model_name: str, timeout: float = 30.0) -> ModelInstance:
        """Acquire available instance"""
        try:
            instance_id = await asyncio.wait_for(
                self._available_queue.get(),
                timeout=timeout
            )
        except asyncio.TimeoutError:
            raise RuntimeError(f"No available instance for model {model_name}")

        instance = self._instances[instance_id]
        instance.status = "in_use"
        instance.last_used = datetime.now()
        logger.info(f"Acquired instance {instance_id}")
        return instance

    async def release(self, instance_id: str) -> None:
        """Release instance back to pool"""
        instance = self._instances.get(instance_id)
        if instance:
            instance.status = "ready"
            instance.last_used = datetime.now()
            await self._available_queue.put(instance_id)
            logger.info(f"Released instance {instance_id}")

    def get_instances(self) -> List[ModelInstance]:
        """Get all instances"""
        return list(self._instances.values())

    def get_instance_status(self) -> List[Dict[str, Any]]:
        """Get instance status"""
        return [
            {
                "instance_id": inst.instance_id,
                "model_name": inst.model_name,
                "device": inst.device,
                "status": inst.status,
                "last_used": inst.last_used.isoformat() if inst.last_used else None
            }
            for inst in self._instances.values()
        ]

    @property
    def available_count(self) -> int:
        """Get count of available instances"""
        return self._available_queue.qsize()


class ModelManager:
    """Model manager for loading and managing models"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self._models: Dict[str, VideoModel] = {}
        self._instance_pool: Optional[ModelInstancePool] = None
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize model manager"""
        if self._initialized:
            return

        self._instance_pool = ModelInstancePool(self.config)
        await self._instance_pool.initialize()
        self._initialized = True
        logger.info("Model manager initialized")

    async def get_instance(self, model_name: str, timeout: float = 30.0) -> ModelInstance:
        """Get available model instance"""
        if not self._initialized:
            await self.initialize()
        return await self._instance_pool.acquire(model_name, timeout)

    async def release_instance(self, instance_id: str) -> None:
        """Release model instance"""
        if self._instance_pool:
            await self._instance_pool.release(instance_id)

    def get_instances(self) -> List[Dict[str, Any]]:
        """Get all model instances"""
        if self._instance_pool:
            return self._instance_pool.get_instance_status()
        return []

    def list_models(self) -> List[Dict[str, Any]]:
        """List available models"""
        return [
            {
                "name": name,
                "type": config.get("type", "yolo"),
                "framework": config.get("framework", "ultralytics"),
                "device": config.get("device", "cpu")
            }
            for name, config in self.config.get("models", {}).items()
        ]

    async def shutdown(self) -> None:
        """Shutdown model manager"""
        for model in self._models.values():
            model.release()
        self._models.clear()
        logger.info("Model manager shutdown")


_model_manager: Optional[ModelManager] = None


async def get_model_manager() -> ModelManager:
    """Get global model manager"""
    global _model_manager
    if _model_manager is None:
        from ..config import get_settings
        settings = get_settings()
        model_config = {
            "gpu_instances": settings.model_pool.gpu_instances,
            "models": settings.models,
            "instance_timeout": settings.model_pool.instance_timeout,
            "max_queue_size": settings.model_pool.max_queue_size
        }
        _model_manager = ModelManager(model_config)
        await _model_manager.initialize()
    return _model_manager