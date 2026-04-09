"""Base model classes"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class ModelInput(BaseModel):
    """Model input"""
    frame: Any
    timestamp: float
    metadata: Dict[str, Any] = {}


class ModelOutput(BaseModel):
    """Model output"""
    predictions: List[Dict[str, Any]]
    processing_time: float
    metadata: Dict[str, Any] = {}


class DetectionResult(BaseModel):
    """Detection result"""
    class_id: int
    class_name: str
    confidence: float
    bbox: List[float]
    tracking_id: Optional[int] = None


class VideoModel(ABC):
    """Abstract video model base class"""

    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize model with configuration"""
        pass

    @abstractmethod
    def infer(self, inputs: List[ModelInput]) -> List[ModelOutput]:
        """Run batch inference"""
        pass

    @abstractmethod
    def release(self) -> None:
        """Release resources"""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Model name"""
        pass


class ModelLoader(ABC):
    """Abstract model loader"""

    @abstractmethod
    async def load_model(self, model_name: str, config: Dict[str, Any]) -> VideoModel:
        """Load model"""
        pass

    @abstractmethod
    async def unload_model(self, model_name: str) -> None:
        """Unload model"""
        pass