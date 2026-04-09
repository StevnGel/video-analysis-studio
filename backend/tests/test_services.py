"""Unit tests for services"""

import pytest
from datetime import datetime


def test_video_source_entity():
    """Test video source entity"""
    from ..src.schemas.video import VideoSource

    video = VideoSource(
        id="test-id",
        name="test.mp4",
        original_name="test.mp4",
        type="file",
        path="/data/videos/test.mp4",
        size=1024000,
        duration=120.0,
        width=1920,
        height=1080,
        fps=30.0,
        codec="h264",
        status="ready",
        tags=["安防"],
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

    assert video.type == "file"
    assert video.status == "ready"
    assert "安防" in video.tags


def test_task_entity():
    """Test task entity"""
    from ..src.services.task_service import Task
    from ..src.schemas.task import (
        InputConfig,
        OutputConfig,
        VideoSourceInput,
        TaskType,
    )

    task = Task(
        task_id="task-001",
        name="Test Task",
        task_type=TaskType.OFFLINE,
        input_config=InputConfig(
            source=VideoSourceInput(type="local", id="video-001")
        ),
        output_config=OutputConfig(type="file", path="/data/output")
    )

    assert task.id == "task-001"
    assert task.name == "Test Task"
    assert task.status.value == "pending"


def test_task_to_response():
    """Test task to response conversion"""
    from ..src.services.task_service import Task
    from ..src.schemas.task import (
        InputConfig,
        OutputConfig,
        VideoSourceInput,
        TaskType,
    )

    task = Task(
        task_id="task-001",
        name="Test Task",
        task_type=TaskType.OFFLINE,
        input_config=InputConfig(
            source=VideoSourceInput(type="local", id="video-001")
        ),
        output_config=OutputConfig(type="file", path="/data/output")
    )

    response = task.to_response()

    assert response.id == "task-001"
    assert response.name == "Test Task"


def test_task_service_create():
    """Test task service creation"""
    from ..src.services.task_service import TaskService
    from ..src.schemas.task import (
        TaskCreate,
        InputConfig,
        OutputConfig,
        VideoSourceInput,
        TaskType,
    )

    service = TaskService()

    task_data = TaskCreate(
        name="New Task",
        task_type=TaskType.OFFLINE,
        input_config=InputConfig(
            source=VideoSourceInput(type="local", id="video-001")
        ),
        output_config=OutputConfig(type="file", path="/data/output")
    )

    import asyncio
    response = asyncio.run(service.create_task(task_data))

    assert response.id.startswith("task-")
    assert response.name == "New Task"


def test_task_service_list():
    """Test task service list"""
    from ..src.services.task_service import TaskService

    service = TaskService()

    import asyncio
    tasks, meta = asyncio.run(service.list_tasks())

    assert isinstance(tasks, list)
    assert meta.total >= 0


def test_video_service_init():
    """Test video service initialization"""
    from ..src.services.video_service import VideoService

    service = VideoService()

    assert isinstance(service._videos, dict)


def test_model_service_list():
    """Test model service list models"""
    from ..src.services.model_service import ModelService

    service = ModelService()
    models = service.list_models()

    assert isinstance(models, list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])