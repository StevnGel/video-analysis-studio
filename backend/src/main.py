import os
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid
import shutil

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data" / "videos"
DATA_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title="Video Analysis Studio API",
    description="视频分析工作台后端 API",
    version="0.1.0"
)

class VideoInfo(BaseModel):
    id: str
    filename: str
    path: str
    size: int
    duration: Optional[float] = None
    width: Optional[int] = None
    height: Optional[int] = None
    status: str = "uploaded"
    created_at: datetime

class VideoListResponse(BaseModel):
    videos: List[VideoInfo]
    total: int

videos_db: List[VideoInfo] = []

@app.get("/")
async def root():
    return {"message": "Video Analysis Studio API", "version": "0.1.0"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/api/videos/upload", response_model=VideoInfo)
async def upload_video(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    file_ext = os.path.splitext(file.filename)[1].lower()
    allowed_exts = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']
    if file_ext not in allowed_exts:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Allowed: {', '.join(allowed_exts)}"
        )
    
    video_id = str(uuid.uuid4())
    safe_filename = f"{video_id}{file_ext}"
    file_path = DATA_DIR / safe_filename
    
    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        file_size = file_path.stat().st_size
        
        video_info = VideoInfo(
            id=video_id,
            filename=file.filename,
            path=str(file_path),
            size=file_size,
            status="uploaded",
            created_at=datetime.now()
        )
        
        videos_db.append(video_info)
        
        return video_info
        
    except Exception as e:
        if file_path.exists():
            file_path.unlink()
        raise HTTPException(status_code=500, detail=f"Failed to upload video: {str(e)}")

@app.get("/api/videos", response_model=VideoListResponse)
async def get_videos():
    return VideoListResponse(videos=videos_db, total=len(videos_db))

@app.get("/api/videos/{video_id}", response_model=VideoInfo)
async def get_video(video_id: str):
    for video in videos_db:
        if video.id == video_id:
            return video
    raise HTTPException(status_code=404, detail="Video not found")

@app.delete("/api/videos/{video_id}")
async def delete_video(video_id: str):
    for i, video in enumerate(videos_db):
        if video.id == video_id:
            file_path = Path(video.path)
            if file_path.exists():
                file_path.unlink()
            videos_db.pop(i)
            return {"message": "Video deleted successfully", "video_id": video_id}
    raise HTTPException(status_code=404, detail="Video not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)