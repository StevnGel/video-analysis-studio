from typing import List
from fastapi import APIRouter, HTTPException, Depends
from src.schemas.video_source import VideoSource, VideoSourceCreate, VideoSourceUpdate
from src.services.video_source_service import video_source_service

router = APIRouter(
    prefix="/api/video-sources",
    tags=["video-sources"],
    responses={404: {"description": "Not found"}},
)


@router.post("", response_model=VideoSource)
def create_video_source(video_source: VideoSourceCreate):
    """创建视频源"""
    try:
        return video_source_service.create_video_source(video_source)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{video_source_id}", response_model=VideoSource)
def get_video_source(video_source_id: str):
    """获取视频源"""
    video_source = video_source_service.get_video_source(video_source_id)
    if not video_source:
        raise HTTPException(status_code=404, detail="视频源不存在")
    return video_source


@router.get("", response_model=List[VideoSource])
def get_video_sources(limit: int = 100, offset: int = 0):
    """获取视频源列表"""
    return video_source_service.get_video_sources(limit, offset)


@router.put("/{video_source_id}", response_model=VideoSource)
def update_video_source(video_source_id: str, video_source: VideoSourceUpdate):
    """更新视频源"""
    updated_video_source = video_source_service.update_video_source(video_source_id, video_source)
    if not updated_video_source:
        raise HTTPException(status_code=404, detail="视频源不存在")
    return updated_video_source


@router.delete("/{video_source_id}")
def delete_video_source(video_source_id: str):
    """删除视频源"""
    success = video_source_service.delete_video_source(video_source_id)
    if not success:
        raise HTTPException(status_code=404, detail="视频源不存在")
    return {"message": "视频源删除成功"}
