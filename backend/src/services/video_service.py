"""Video source service"""

import logging
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import BinaryIO, List, Optional
from uuid import uuid4

from ..config import get_settings
from ..exceptions import (
    VideoFormatError,
    VideoNotFoundError,
    VideoUploadError,
)
from ..schemas.common import PaginationMeta
from ..schemas.video import VideoSource

logger = logging.getLogger(__name__)

SUPPORTED_FORMATS = {".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv", ".webm"}
MAX_FILE_SIZE = 2 * 1024 * 1024 * 1024  # 2GB


class VideoService:
    """Video source management service"""

    def __init__(self):
        self._videos: dict[str, VideoSource] = {}
        self._storage_path: Optional[Path] = None

    def _get_storage_path(self) -> Path:
        """Get storage path"""
        if self._storage_path is None:
            settings = get_settings()
            self._storage_path = Path(settings.storage.video_dir)
            self._storage_path.mkdir(parents=True, exist_ok=True)
        return self._storage_path

    def _get_video_info(self, file_path: Path) -> dict:
        """Get video information"""
        file_size = file_path.stat().st_size

        import cv2
        cap = cv2.VideoCapture(str(file_path))
        if not cap.isOpened():
            return {
                "width": 0,
                "height": 0,
                "fps": 0.0,
                "duration": 0.0,
                "codec": "unknown"
            }

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        duration = frame_count / fps if fps > 0 else 0

        fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
        codec = chr(fourcc & 0xFF) + chr((fourcc >> 8) & 0xFF) + chr((fourcc >> 16) & 0xFF) + chr((fourcc >> 24) & 0xFF)

        cap.release()
        return {
            "width": width,
            "height": height,
            "fps": fps,
            "duration": duration,
            "codec": codec,
            "size": file_size
        }

    async def upload_video(
        self,
        file: BinaryIO,
        filename: str,
        name: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> VideoSource:
        """Upload video file"""
        ext = Path(filename).suffix.lower()
        if ext not in SUPPORTED_FORMATS:
            raise VideoFormatError(ext)

        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)

        if file_size > MAX_FILE_SIZE:
            raise VideoUploadError(f"File size {file_size} exceeds max {MAX_FILE_SIZE}")

        video_id = str(uuid4())
        storage_dir = self._get_storage_path()
        dest_filename = f"{video_id}{ext}"
        dest_path = storage_dir / dest_filename

        try:
            with open(dest_path, "wb") as dest:
                shutil.copyfileobj(file, dest)
        except Exception as e:
            raise VideoUploadError(f"Failed to save file: {str(e)}")

        video_info = self._get_video_info(dest_path)

        now = datetime.now()
        video = VideoSource(
            id=video_id,
            name=name or filename,
            original_name=filename,
            type="file",
            path=str(dest_path),
            size=video_info["size"],
            duration=video_info["duration"],
            width=video_info["width"],
            height=video_info["height"],
            fps=video_info["fps"],
            codec=video_info["codec"],
            status="ready",
            tags=tags,
            created_at=now,
            updated_at=now
        )

        self._videos[video_id] = video
        logger.info(f"Video uploaded: {video_id} - {filename}")
        return video

    def get_video(self, video_id: str) -> VideoSource:
        """Get video by ID"""
        video = self._videos.get(video_id)
        if not video:
            raise VideoNotFoundError(video_id)
        return video

    def list_videos(
        self,
        page: int = 1,
        page_size: int = 20,
        status: Optional[str] = None,
        tags: Optional[str] = None
    ) -> tuple[List[VideoSource], PaginationMeta]:
        """List videos with pagination"""
        videos = list(self._videos.values())

        if status:
            videos = [v for v in videos if v.status == status]

        if tags:
            tag_list = tags.split(",")
            videos = [v for v in videos if v.tags and any(t in v.tags for t in tag_list)]

        total = len(videos)
        total_pages = (total + page_size - 1) // page_size if total > 0 else 1

        start = (page - 1) * page_size
        end = start + page_size
        paginated = videos[start:end]

        meta = PaginationMeta(
            page=page,
            page_size=page_size,
            total=total,
            total_pages=total_pages
        )

        return paginated, meta

    async def delete_video(self, video_id: str) -> str:
        """Delete video"""
        video = self._videos.get(video_id)
        if not video:
            raise VideoNotFoundError(video_id)

        video_path = Path(video.path)
        if video_path.exists():
            video_path.unlink()

        del self._videos[video_id]
        logger.info(f"Video deleted: {video_id}")
        return video_id


_video_service: Optional[VideoService] = None


def get_video_service() -> VideoService:
    """Get global video service"""
    global _video_service
    if _video_service is None:
        _video_service = VideoService()
    return _video_service