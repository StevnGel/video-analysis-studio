from typing import List
from fastapi import APIRouter, HTTPException, Depends
from src.schemas.task import Task, TaskCreate, TaskUpdate
from src.services.task_service import task_service

router = APIRouter(
    prefix="/api/tasks",
    tags=["tasks"],
    responses={404: {"description": "Not found"}},
)


@router.post("", response_model=Task)
def create_task(task: TaskCreate):
    """创建任务"""
    try:
        return task_service.create_task(task)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{task_id}", response_model=Task)
def get_task(task_id: str):
    """获取任务"""
    task = task_service.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    return task


@router.get("", response_model=List[Task])
def get_tasks(limit: int = 100, offset: int = 0):
    """获取任务列表"""
    return task_service.get_tasks(limit, offset)


@router.put("/{task_id}", response_model=Task)
def update_task(task_id: str, task: TaskUpdate):
    """更新任务"""
    updated_task = task_service.update_task(task_id, task)
    if not updated_task:
        raise HTTPException(status_code=404, detail="任务不存在")
    return updated_task


@router.delete("/{task_id}")
def delete_task(task_id: str):
    """删除任务"""
    success = task_service.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="任务不存在")
    return {"message": "任务删除成功"}
