"""Model service"""

import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class ModelService:
    """Model management service"""

    def __init__(self):
        self._models: Dict[str, Dict] = {}

    def list_models(self) -> List[Dict]:
        """List available models"""
        from ..config import get_settings
        settings = get_settings()

        models = []
        for name, config in settings.models.items():
            models.append({
                "name": name,
                "type": config.get("type", "yolo"),
                "framework": config.get("framework", "ultralytics"),
                "description": f"{name} model for video analysis"
            })
        return models

    def get_model(self, model_name: str) -> Dict:
        """Get model details"""
        from ..config import get_settings
        from ..exceptions import ModelNotFoundError

        settings = get_settings()
        model_config = settings.models.get(model_name)

        if not model_config:
            raise ModelNotFoundError(model_name)

        return {
            "name": model_name,
            "type": model_config.get("type", "yolo"),
            "framework": model_config.get("framework", "ultralytics"),
            "config": model_config
        }

    async def get_instances(self) -> List[Dict]:
        """Get model instances"""
        from ..models import get_model_manager
        manager = await get_model_manager()
        return manager.get_instances()


_model_service: Optional[ModelService] = None


def get_model_service() -> ModelService:
    """Get global model service"""
    global _model_service
    if _model_service is None:
        _model_service = ModelService()
    return _model_service