"""Video Analysis Studio Backend - Main Application"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import videos_router, tasks_router, models_router
from .config import get_settings
from .utils import setup_logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    logger.info("Starting Video Analysis Studio Backend...")

    settings = get_settings()
    setup_logging(settings.logging.level, settings.logging.format)

    logger.info(f"App: {settings.app.name} v{settings.app.version}")

    yield

    logger.info("Shutting down Video Analysis Studio Backend...")


app = FastAPI(
    title="Video Analysis Studio",
    description="Video analysis backend API for video processing and analysis tasks",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(videos_router, prefix="/api/v1")
app.include_router(tasks_router, prefix="/api/v1")
app.include_router(models_router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint"""
    settings = get_settings()
    return {
        "name": settings.app.name,
        "version": settings.app.version,
        "status": "running"
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        "src.main:app",
        host=settings.server.host,
        port=settings.server.port,
        reload=settings.server.reload
    )