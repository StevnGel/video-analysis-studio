"""Task service"""

import asyncio
import logging
from datetime import datetime
from typing import Optional
from uuid import uuid4

from ..exceptions import TaskNotFoundError, TaskStartError, TaskStopError
from ..schemas.common import PaginationMeta
from ..schemas.task import (
    InputConfig,
    ModelConfig,
    OutputConfig,
    TaskCreate,
    TaskResponse,
    TaskStatistics,
    TaskStatus,
    TaskType,
)

logger = logging.getLogger(__name__)


class Task:
    """Task entity"""

    def __init__(
        self,
        task_id: str,
        name: str,
        task_type: TaskType,
        input_config: InputConfig,
        output_config: OutputConfig,
        model_config: Optional[ModelConfig] = None,
        priority: int = 50
    ):
        self.id = task_id
        self.name = name
        self.task_type = task_type
        self.input_config = input_config
        self.output_config = output_config
        self.model_config = model_config
        self.priority = priority
        self.status = TaskStatus.PENDING
        self.progress = 0.0
        self.gpu_device: Optional[str] = None
        self.result_url: Optional[str] = None
        self.video_source_id: Optional[str] = None
        self.created_at = datetime.now()
        self.started_at: Optional[datetime] = None
        self.completed_at: Optional[datetime] = None
        self.error_message: Optional[str] = None
        self.statistics = TaskStatistics()
        self._running = False

    def to_response(self) -> TaskResponse:
        """Convert to response"""
        return TaskResponse(
            id=self.id,
            name=self.name,
            task_type=self.task_type.value,
            video_source_id=self.input_config.source.id if self.input_config.source else None,
            input_config=self.input_config,
            output_config=self.output_config,
            model_config=self.model_config,
            status=self.status,
            progress=self.progress,
            gpu_device=self.gpu_device,
            result_url=self.result_url,
            priority=self.priority,
            created_at=self.created_at,
            started_at=self.started_at,
            completed_at=self.completed_at,
            error_message=self.error_message,
            statistics=self.statistics
        )


class TaskService:
    """Task management service"""

    def __init__(self):
        self._tasks: dict[str, Task] = {}
        self._running_tasks: dict[str, asyncio.Task] = {}

    async def create_task(self, task_data: TaskCreate) -> TaskResponse:
        """Create task"""
        task_id = f"task-{uuid4().hex[:8]}"

        if task_data.input_config.source.type == "local" and task_data.input_config.source.id:
            video_source_id = task_data.input_config.source.id
        else:
            video_source_id = None

        task = Task(
            task_id=task_id,
            name=task_data.name,
            task_type=task_data.task_type,
            input_config=task_data.input_config,
            output_config=task_data.output_config,
            model_config=task_data.model_config,
            priority=task_data.priority
        )
        task.video_source_id = video_source_id

        if task_data.model_config:
            task.status = TaskStatus.PENDING_WITH_INFERENCE

        self._tasks[task_id] = task
        logger.info(f"Task created: {task_id}")
        return task.to_response()

    def get_task(self, task_id: str) -> TaskResponse:
        """Get task by ID"""
        task = self._tasks.get(task_id)
        if not task:
            raise TaskNotFoundError(task_id)
        return task.to_response()

    def list_tasks(
        self,
        page: int = 1,
        page_size: int = 20,
        status: Optional[str] = None,
        task_type: Optional[str] = None
    ) -> tuple[list[TaskResponse], PaginationMeta]:
        """List tasks with pagination"""
        tasks = list(self._tasks.values())

        if status:
            tasks = [t for t in tasks if t.status.value == status]

        if task_type:
            tasks = [t for t in tasks if t.task_type.value == task_type]

        tasks.sort(key=lambda t: t.created_at, reverse=True)

        total = len(tasks)
        total_pages = (total + page_size - 1) // page_size if total > 0 else 1

        start = (page - 1) * page_size
        end = start + page_size
        paginated = tasks[start:end]

        meta = PaginationMeta(
            page=page,
            page_size=page_size,
            total=total,
            total_pages=total_pages
        )

        return [t.to_response() for t in paginated], meta

    async def start_task(self, task_id: str) -> TaskResponse:
        """Start task"""
        task = self._tasks.get(task_id)
        if not task:
            raise TaskNotFoundError(task_id)

        if task.status in (TaskStatus.RUNNING, TaskStatus.COMPLETED):
            raise TaskStartError(f"Task is already {task.status.value}")

        task.status = TaskStatus.RUNNING
        task.started_at = datetime.now()
        task.gpu_device = "cpu"

        logger.info(f"Task started: {task_id}")
        return task.to_response()

    async def stop_task(self, task_id: str) -> TaskResponse:
        """Stop task"""
        task = self._tasks.get(task_id)
        if not task:
            raise TaskNotFoundError(task_id)

        if task.status not in (TaskStatus.RUNNING, TaskStatus.PAUSED):
            raise TaskStopError(f"Task is not running (status: {task.status.value})")

        task.status = TaskStatus.CANCELLED

        logger.info(f"Task stopped: {task_id}")
        return task.to_response()

    async def delete_task(self, task_id: str) -> str:
        """Delete task"""
        task = self._tasks.get(task_id)
        if not task:
            raise TaskNotFoundError(task_id)

        del self._tasks[task_id]
        logger.info(f"Task deleted: {task_id}")
        return task_id

    def get_output_url(self, task_id: str) -> tuple[str, str]:
        """Get task output URL"""
        task = self._tasks.get(task_id)
        if not task:
            raise TaskNotFoundError(task_id)

        output_type = task.output_config.type
        if output_type == "file":
            output_url = task.result_url or f"/data/output/{task_id}.mp4"
        elif output_type == "rtmp":
            output_url = task.output_config.rtmp_url or f"rtmp://localhost/live/{task_id}"
        elif output_type == "hls":
            output_url = f"/data/hls/{task_id}/playlist.m3u8"
        else:
            output_url = ""

        return output_url, output_type


_task_service: Optional[TaskService] = None


def get_task_service() -> TaskService:
    """Get global task service"""
    global _task_service
    if _task_service is None:
        _task_service = TaskService()
    return _task_service