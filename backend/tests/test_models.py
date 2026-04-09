"""Unit tests for models"""

import pytest


def test_yolo_model_initialize():
    """Test YOLO model initialization"""
    from ..src.models.yolo import YOLOModel

    model = YOLOModel()
    config = {
        "model_path": "yolov8n.pt",
        "conf_threshold": 0.25,
        "iou_threshold": 0.45
    }

    model.initialize(config)

    assert model.name == "yolo_v8"
    assert model._initialized is True


def test_yolo_model_infer():
    """Test YOLO model inference"""
    from ..src.models.yolo import YOLOModel
    from ..src.models.base import ModelInput
    import numpy as np

    model = YOLOModel()
    model.initialize({})

    inputs = [
        ModelInput(frame=np.zeros((640, 640, 3), timestamp=0.0),
        ModelInput(frame=np.zeros((640, 640, 3), timestamp=0.033)
    ]

    outputs = model.infer(inputs)

    assert len(outputs) == 2
    assert isinstance(outputs[0].predictions, list)


def test_yolo_model_release():
    """Test YOLO model release"""
    from ..src.models.yolo import YOLOModel

    model = YOLOModel()
    model.initialize({})

    model.release()

    assert model._initialized is False


def test_model_instance_pool():
    """Test model instance pool"""
    from ..src.models.manager import ModelInstancePool

    config = {
        "gpu_instances": [
            {"device": "cpu", "instance_count": 2, "model": "yolo_v8"}
        ]
    }

    import asyncio

    async def test_pool():
        pool = ModelInstancePool(config)
        await pool.initialize()

        instances = pool.get_instances()
        assert len(instances) == 2

        return pool

    pool = asyncio.run(test_pool())


def test_model_instance_creation():
    """Test model instance creation"""
    from ..src.models.manager import ModelInstance
    from datetime import datetime

    instance = ModelInstance(
        instance_id="inst-001",
        model_name="yolo_v8",
        model_type="yolo",
        device="cpu",
        status="ready",
        load_time=datetime.now()
    )

    assert instance.model_name == "yolo_v8"
    assert instance.status == "ready"


def test_detection_result_model():
    """Test detection result with model"""
    from ..src.models.base import DetectionResult

    result = DetectionResult(
        class_id=0,
        class_name="person",
        confidence=0.92,
        bbox=[10, 20, 100, 200]
    )

    assert result.confidence > 0.9
    assert result.bbox == [10, 20, 100, 200]


def test_model_output():
    """Test model output"""
    from ..src.models.base import ModelOutput

    output = ModelOutput(
        predictions=[
            {"class_id": 0, "confidence": 0.95}
        ],
        processing_time=10.5,
        metadata={"timestamp": 0.0}
    )

    assert len(output.predictions) == 1
    assert output.processing_time > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])