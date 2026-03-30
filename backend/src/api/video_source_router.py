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


@router.post("/{video_source_id}/start-rtmp")
def start_mp4_http_to_rtmp_stream(video_source_id: str, rtmp_url: dict):
    """启动 MP4 HTTP 到 RTMP 的转流"""
    try:
        rtmp_url_value = rtmp_url.get("rtmp_url")
        if not rtmp_url_value:
            raise HTTPException(status_code=400, detail="缺少 rtmp_url 参数")
        
        success = video_source_service.start_mp4_http_to_rtmp_stream(video_source_id, rtmp_url_value)
        if not success:
            raise HTTPException(status_code=400, detail="启动转流失败")
        
        return {"message": "转流启动成功"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{video_source_id}/stop-rtmp")
def stop_mp4_http_to_rtmp_stream(video_source_id: str):
    """停止 MP4 HTTP 到 RTMP 的转流"""
    try:
        success = video_source_service.stop_mp4_http_to_rtmp_stream(video_source_id)
        if not success:
            raise HTTPException(status_code=400, detail="停止转流失败")
        
        return {"message": "转流停止成功"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
