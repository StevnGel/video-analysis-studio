from typing import List, Optional
from src.schemas.video_source import VideoSource, VideoSourceCreate, VideoSourceUpdate
from src.utils.supabase_client import supabase
from src.utils.gstreamer_manager import gstreamer_manager


class VideoSourceService:
    """视频源服务类"""
    
    def __init__(self):
        """初始化视频源服务"""
        self.table_name = "video_sources"
    
    def create_video_source(self, video_source: VideoSourceCreate) -> VideoSource:
        """创建视频源
        
        Args:
            video_source: 视频源创建模型
            
        Returns:
            VideoSource: 创建的视频源
        """
        # 转换为字典并插入数据
        data = video_source.model_dump()
        response = supabase.table(self.table_name).insert(data).execute()
        
        # 检查响应
        if response.data:
            return VideoSource(**response.data[0])
        else:
            raise Exception("创建视频源失败")
    
    def get_video_source(self, video_source_id: str) -> Optional[VideoSource]:
        """获取视频源
        
        Args:
            video_source_id: 视频源ID
            
        Returns:
            Optional[VideoSource]: 视频源对象
        """
        response = supabase.table(self.table_name).select("*").eq("id", video_source_id).execute()
        
        if response.data:
            return VideoSource(**response.data[0])
        else:
            return None
    
    def get_video_sources(self, limit: int = 100, offset: int = 0) -> List[VideoSource]:
        """获取视频源列表
        
        Args:
            limit: 限制数量
            offset: 偏移量
            
        Returns:
            List[VideoSource]: 视频源列表
        """
        response = supabase.table(self.table_name).select("*").limit(limit).offset(offset).execute()
        
        if response.data:
            return [VideoSource(**item) for item in response.data]
        else:
            return []
    
    def update_video_source(self, video_source_id: str, video_source: VideoSourceUpdate) -> Optional[VideoSource]:
        """更新视频源
        
        Args:
            video_source_id: 视频源ID
            video_source: 视频源更新模型
            
        Returns:
            Optional[VideoSource]: 更新后的视频源
        """
        # 转换为字典，排除None值
        data = video_source.model_dump(exclude_unset=True)
        response = supabase.table(self.table_name).update(data).eq("id", video_source_id).execute()
        
        if response.data:
            return VideoSource(**response.data[0])
        else:
            return None
    
    def delete_video_source(self, video_source_id: str) -> bool:
        """删除视频源
        
        Args:
            video_source_id: 视频源ID
            
        Returns:
            bool: 是否删除成功
        """
        # 先停止可能正在运行的转流
        self.stop_mp4_http_to_rtmp_stream(video_source_id)
        
        response = supabase.table(self.table_name).delete().eq("id", video_source_id).execute()
        return len(response.data) > 0
    
    def start_mp4_http_to_rtmp_stream(self, video_source_id: str, rtmp_url: str) -> bool:
        """启动 MP4 HTTP 到 RTMP 的转流
        
        Args:
            video_source_id: 视频源ID
            rtmp_url: RTMP 目标地址
            
        Returns:
            bool: 是否启动成功
        """
        # 获取视频源信息
        video_source = self.get_video_source(video_source_id)
        if not video_source:
            return False
        
        # 检查是否是HTTP MP4地址
        if not video_source.url.startswith(('http://', 'https://')):
            return False
        
        # 创建并启动转流管道
        pipeline_id = f"mp4_http_to_rtmp_{video_source_id}"
        
        # 先停止可能存在的管道
        if gstreamer_manager.get_pipeline_state(pipeline_id):
            gstreamer_manager.stop_pipeline(pipeline_id)
            gstreamer_manager.delete_pipeline(pipeline_id)
        
        # 创建新管道
        if not gstreamer_manager.create_mp4_http_to_rtmp_pipeline(pipeline_id, video_source.url, rtmp_url):
            return False
        
        # 启动管道
        return gstreamer_manager.start_pipeline(pipeline_id)
    
    def stop_mp4_http_to_rtmp_stream(self, video_source_id: str) -> bool:
        """停止 MP4 HTTP 到 RTMP 的转流
        
        Args:
            video_source_id: 视频源ID
            
        Returns:
            bool: 是否停止成功
        """
        pipeline_id = f"mp4_http_to_rtmp_{video_source_id}"
        return gstreamer_manager.delete_pipeline(pipeline_id)


# 创建视频源服务实例
video_source_service = VideoSourceService()
