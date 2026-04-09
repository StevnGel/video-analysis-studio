"""Video API routes"""

import logging
from typing import List, Optional

from fastapi import APIRouter, File, Form, HTTPException, Query, UploadFile
from fastapi.responses import JSONResponse

from ..schemas.common import PaginationMeta
from ..schemas.video import (
    VideoDeleteResponse,
    VideoListResponse,
    VideoSource,
    VideoUploadResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/videos", tags=["videos"])


@router.post("/upload", response_model=VideoUploadResponse, status_code=201)
async def upload_video(
    file: UploadFile = File(...),
    name: Optional[str] = Form(None),
    tags: Optional[str] = Form(None)
):
    """Upload video file"""
    from ..services import get_video_service

    service = get_video_service()

    tag_list = []
    if tags:
        try:
            import json
            tag_list = json.loads(tags)
        except:
            tag_list = [t.strip() for t in tags.split(",")]

    try:
        video = await service.upload_video(
            file=file.file,
            filename=file.filename,
            name=name,
            tags=tag_list if tag_list else None
        )
        return VideoUploadResponse(
            id=video.id,
            name=video.name,
            original_name=video.original_name,
            type=video.type,
            path=video.path,
            size=video.size,
            duration=video.duration,
            width=video.width,
            height=video.height,
            fps=video.fps,
            codec=video.codec,
            status=video.status,
            tags=video.tags,
            created_at=video.created_at,
            updated_at=video.updated_at
        )
    except Exception as e:
        logger.error(f"Video upload failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("", response_model=VideoListResponse)
async def list_videos(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[str] = Query(None),
    tags: Optional[str] = Query(None)
):
    """Get video list"""
    from ..services import get_video_service

    service = get_video_service()
    videos, meta = service.list_videos(page, page_size, status, tags)

    return VideoListResponse(
        videos=[
            VideoSource(
                id=v.id,
                name=v.name,
                original_name=v.original_name,
                type=v.type,
                path=v.path,
                size=v.size,
                duration=v.duration,
                width=v.width,
                height=v.height,
                fps=v.fps,
                codec=v.codec,
                status=v.status,
                tags=v.tags,
                created_at=v.created_at,
                updated_at=v.updated_at
            )
            for v in videos
        ],
        pagination=PaginationMeta(
            page=meta.page,
            page_size=meta.page_size,
            total=meta.total,
            total_pages=meta.total_pages
        )
    )


@router.get("/{video_id}", response_model=VideoSource)
async def get_video(video_id: str):
    """Get video details"""
    from ..services import get_video_service
    from ..exceptions import VideoNotFoundError

    service = get_video_service()
    try:
        video = service.get_video(video_id)
        return VideoSource(
            id=video.id,
            name=video.name,
            original_name=video.original_name,
            type=video.type,
            path=video.path,
            size=video.size,
            duration=video.duration,
            width=video.width,
            height=video.height,
            fps=video.fps,
            codec=video.codec,
            status=video.status,
            tags=video.tags,
            metadata=video.metadata,
            created_at=video.created_at,
            updated_at=video.updated_at
        )
    except VideoNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.delete("/{video_id}", response_model=VideoDeleteResponse)
async def delete_video(video_id: str):
    """Delete video"""
    from ..services import get_video_service
    from ..exceptions import VideoNotFoundError

    service = get_video_service()
    try:
        deleted_id = await service.delete_video(video_id)
        return VideoDeleteResponse(deleted_id=deleted_id)
    except VideoNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)