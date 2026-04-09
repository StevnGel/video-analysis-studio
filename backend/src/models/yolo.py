"""YOLO model implementation"""

import logging
from typing import Any, Dict, List, Optional

import numpy as np

from .base import DetectionResult, ModelInput, ModelOutput, VideoModel

logger = logging.getLogger(__name__)


class YOLOModel(VideoModel):
    """YOLO model implementation using Ultralytics"""

    def __init__(self):
        self._model: Optional[Any] = None
        self._config: Dict[str, Any] = {}
        self._initialized = False

    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize YOLO model"""
        self._config = config
        model_path = config.get("model_path", "yolov8n.pt")

        try:
            from ultralytics import YOLO
            self._model = YOLO(model_path)
            self._initialized = True
            logger.info(f"YOLO model initialized with {model_path}")
        except ImportError:
            logger.warning("Ultralytics not installed, using mock YOLO")
            self._model = None
            self._initialized = True

    def infer(self, inputs: List[ModelInput]) -> List[ModelOutput]:
        """Run batch inference"""
        if not self._initialized:
            raise RuntimeError("Model not initialized")

        if self._model is None:
            return self._mock_infer(inputs)

        frames = [inp.frame for inp in inputs]
        timestamps = [inp.timestamp for inp in inputs]

        results = self._model(
            frames,
            conf=self._config.get("conf_threshold", 0.25),
            iou=self._config.get("iou_threshold", 0.45),
            verbose=False
        )

        outputs = []
        for idx, result in enumerate(results):
            detections = []
            if result.boxes is not None and len(result.boxes) > 0:
                for box in result.boxes:
                    detections.append({
                        "class_id": int(box.cls[0]),
                        "class_name": result.names[int(box.cls[0])],
                        "confidence": float(box.conf[0]),
                        "bbox": box.xyxy[0].tolist()
                    })

            outputs.append(ModelOutput(
                predictions=detections,
                processing_time=result.speed.get("inference", 0) if hasattr(result, "speed") else 0,
                metadata={"timestamp": timestamps[idx]}
            ))

        return outputs

    def _mock_infer(self, inputs: List[ModelInput]) -> List[ModelOutput]:
        """Mock inference for testing without YOLO"""
        outputs = []
        for inp in inputs:
            outputs.append(ModelOutput(
                predictions=[],
                processing_time=0.0,
                metadata={"timestamp": inp.timestamp}
            ))
        return outputs

    def release(self) -> None:
        """Release resources"""
        if self._model is not None:
            del self._model
            self._model = None
        self._initialized = False
        logger.info("YOLO model released")

    @property
    def name(self) -> str:
        return "yolo_v8"


def create_yolo_model(config: Dict[str, Any]) -> YOLOModel:
    """Create YOLO model instance"""
    model = YOLOModel()
    model.initialize(config)
    return model