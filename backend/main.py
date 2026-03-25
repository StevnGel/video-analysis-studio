from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config.config import settings
from src.api import video_source_router, model_router, task_router, event_router, config_router

# 创建 FastAPI 应用
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="视频分析工作台 API"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(video_source_router.router)
app.include_router(model_router.router)
app.include_router(task_router.router)
app.include_router(event_router.router)
app.include_router(config_router.router)


@app.get("/")
def read_root():
    """根路径"""
    return {
        "message": "Welcome to Video Analysis Studio API",
        "version": settings.app_version,
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """健康检查"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
