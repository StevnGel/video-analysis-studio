from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """应用配置类"""
    # 应用配置
    app_name: str = "Video Analysis Studio"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # 服务器配置
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Supabase 配置 (可选)
    supabase_url: Optional[str] = ""
    supabase_key: Optional[str] = ""
    
    # GStreamer 配置
    gst_buffer_size: int = 1024
    gst_frame_rate: int = 30
    
    # 并发配置
    thread_pool_size: int = 4
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# 创建配置实例
settings = Settings()
