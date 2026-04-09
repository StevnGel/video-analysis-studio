"""Unit tests for Video Analysis Studio Backend"""

import pytest


def test_config_loader():
    """Test configuration loader"""
    from ..src.config import ConfigLoader

    loader = ConfigLoader()
    settings = loader.load()

    assert settings.app.name == "video-analysis-studio"
    assert settings.app.version == "1.0.0"


def test_config_resolve_env_vars():
    """Test environment variable resolution"""
    import os
    from ..src.config import ConfigLoader

    os.environ["TEST_VAR"] = "test_value"

    loader = ConfigLoader()
    template = "prefix_${TEST_VAR}_suffix"
    result = loader.resolve_placeholders(template, {"TEST_VAR": "resolved"})

    assert result == "prefix_resolved_suffix"


def test_settings_defaults():
    """Test default settings values"""
    from ..src.config import Settings

    settings = Settings()

    assert settings.server.host == "0.0.0.0"
    assert settings.server.port == 8000
    assert settings.model_pool.instance_timeout == 300


def test_pagination_meta():
    """Test pagination metadata"""
    from ..src.schemas.common import PaginationMeta

    meta = PaginationMeta(page=1, page_size=20, total=100, total_pages=5)

    assert meta.page == 1
    assert meta.page_size == 20
    assert meta.total == 100
    assert meta.total_pages == 5


def test_video_source_schema():
    """Test video source schema"""
    from datetime import datetime
    from ..src.schemas.video import VideoSource

    video = VideoSource(
        id="test-id",
        name="test.mp4",
        original_name="test.mp4",
        type="file",
        path="/data/test.mp4",
        size=1024,
        duration=10.0,
        width=1920,
        height=1080,
        fps=30.0,
        codec="h264",
        status="ready",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

    assert video.id == "test-id"
    assert video.status == "ready"


def test_task_create_schema():
    """Test task create schema"""
    from ..src.schemas.task import TaskCreate, InputConfig, OutputConfig
    from ..src.schemas.task import VideoSourceInput
    from ..src.schemas.task import TaskType

    task = TaskCreate(
        name="Test Task",
        task_type=TaskType.OFFLINE,
        input_config=InputConfig(
            source=VideoSourceInput(type="local", id="video-id")
        ),
        output_config=OutputConfig(type="file", path="/data/output")
    )

    assert task.name == "Test Task"
    assert task.task_type == TaskType.OFFLINE


def test_task_status_enum():
    """Test task status enumeration"""
    from ..src.schemas.task import TaskStatus

    assert TaskStatus.PENDING.value == "pending"
    assert TaskStatus.RUNNING.value == "running"
    assert TaskStatus.COMPLETED.value == "completed"


def test_model_config_schema():
    """Test model configuration schema"""
    from ..src.schemas.task import ModelConfig, ModelItem, InferenceConfig, DrawConfig

    config = ModelConfig(
        parallel=True,
        models=[
            ModelItem(
                name="yolo_v8",
                config=InferenceConfig(confidence_threshold=0.5),
                enabled=True,
                for_display=True,
                draw_config=DrawConfig(draw_bbox=True)
            )
        ]
    )

    assert config.parallel is True
    assert len(config.models) == 1
    assert config.models[0].name == "yolo_v8"


def test_video_model_base():
    """Test video model base class"""
    from ..src.models.base import VideoModel, ModelInput

    class DummyModel(VideoModel):
        @property
        def name(self) -> str:
            return "dummy"

        def initialize(self, config):
            pass

        def infer(self, inputs):
            return []

        def release(self):
            pass

    model = DummyModel()
    assert model.name == "dummy"


def test_detection_result():
    """Test detection result"""
    from ..src.models.base import DetectionResult

    detection = DetectionResult(
        class_id=0,
        class_name="person",
        confidence=0.95,
        bbox=[100, 200, 150, 350]
    )

    assert detection.class_id == 0
    assert detection.class_name == "person"
    assert detection.confidence == 0.95


def test_config_loader_resolve_env():
    """Test config loader environment variable resolution"""
    import os
    from ..src.config import ConfigLoader

    os.environ["VIDEO_DIR"] = "/custom/video"

    loader = ConfigLoader()
    result = loader._resolve_env_vars({"path": "${VIDEO_DIR}"})

    assert result["path"] == "/custom/video"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])