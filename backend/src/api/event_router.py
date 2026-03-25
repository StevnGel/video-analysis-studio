from typing import List
from fastapi import APIRouter, HTTPException, Depends
from src.schemas.event import Event, EventCreate, EventUpdate
from src.services.event_service import event_service

router = APIRouter(
    prefix="/api/events",
    tags=["events"],
    responses={404: {"description": "Not found"}},
)


@router.post("", response_model=Event)
def create_event(event: EventCreate):
    """创建事件"""
    try:
        return event_service.create_event(event)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{event_id}", response_model=Event)
def get_event(event_id: str):
    """获取事件"""
    event = event_service.get_event(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="事件不存在")
    return event


@router.get("", response_model=List[Event])
def get_events(limit: int = 100, offset: int = 0):
    """获取事件列表"""
    return event_service.get_events(limit, offset)


@router.get("/task/{task_id}", response_model=List[Event])
def get_events_by_task(task_id: str, limit: int = 100, offset: int = 0):
    """根据任务获取事件列表"""
    return event_service.get_events_by_task(task_id, limit, offset)


@router.put("/{event_id}", response_model=Event)
def update_event(event_id: str, event: EventUpdate):
    """更新事件"""
    updated_event = event_service.update_event(event_id, event)
    if not updated_event:
        raise HTTPException(status_code=404, detail="事件不存在")
    return updated_event


@router.delete("/{event_id}")
def delete_event(event_id: str):
    """删除事件"""
    success = event_service.delete_event(event_id)
    if not success:
        raise HTTPException(status_code=404, detail="事件不存在")
    return {"message": "事件删除成功"}
