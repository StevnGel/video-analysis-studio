"""Task API routes"""

import logging
from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from ..schemas.common import PaginationMeta
from ..schemas.task import (
    TaskCreate,
    TaskListResponse,
    TaskOutputResponse,
    TaskResponse,
    TaskStartResponse,
    TaskStopResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=TaskResponse, status_code=201)
async def create_task(task_data: TaskCreate):
    """Create analysis task"""
    from ..services import get_task_service

    service = get_task_service()
    try:
        task = await service.create_task(task_data)
        return task
    except Exception as e:
        logger.error(f"Task creation failed: {e}")
        raise HTTPException(status_code=422, detail=str(e))


@router.get("", response_model=TaskListResponse)
async def list_tasks(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[str] = Query(None),
    task_type: Optional[str] = Query(None)
):
    """Get task list"""
    from ..services import get_task_service

    service = get_task_service()
    tasks, meta = service.list_tasks(page, page_size, status, task_type)

    return TaskListResponse(
        tasks=tasks,
        pagination=PaginationMeta(
            page=meta.page,
            page_size=meta.page_size,
            total=meta.total,
            total_pages=meta.total_pages
        )
    )


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str):
    """Get task details"""
    from ..services import get_task_service
    from ..exceptions import TaskNotFoundError

    service = get_task_service()
    try:
        return service.get_task(task_id)
    except TaskNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.post("/{task_id}/start", response_model=TaskStartResponse)
async def start_task(task_id: str):
    """Start task"""
    from ..services import get_task_service
    from ..exceptions import TaskNotFoundError

    service = get_task_service()
    try:
        task = await service.start_task(task_id)
        return TaskStartResponse(
            task_id=task.id,
            status=task.status.value,
            started_at=task.started_at
        )
    except TaskNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.post("/{task_id}/stop", response_model=TaskStopResponse)
async def stop_task(task_id: str):
    """Stop task"""
    from ..services import get_task_service
    from ..exceptions import TaskNotFoundError

    service = get_task_service()
    try:
        task = await service.stop_task(task_id)
        return TaskStopResponse(
            task_id=task.id,
            status=task.status.value
        )
    except TaskNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.delete("/{task_id}")
async def delete_task(task_id: str):
    """Delete task"""
    from ..services import get_task_service
    from ..exceptions import TaskNotFoundError

    service = get_task_service()
    try:
        deleted_id = await service.delete_task(task_id)
        return {"deleted_id": deleted_id}
    except TaskNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.get("/{task_id}/output", response_model=TaskOutputResponse)
async def get_task_output(task_id: str):
    """Get task output URL"""
    from ..services import get_task_service
    from ..exceptions import TaskNotFoundError

    service = get_task_service()
    try:
        output_url, output_type = service.get_output_url(task_id)
        return TaskOutputResponse(output_url=output_url, output_type=output_type)
    except TaskNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)