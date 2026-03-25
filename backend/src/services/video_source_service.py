from typing import List, Optional
from src.schemas.video_source import VideoSource, VideoSourceCreate, VideoSourceUpdate
from src.utils.supabase_client import supabase


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
        response = supabase.table(self.table_name).delete().eq("id", video_source_id).execute()
        return len(response.data) > 0


# 创建视频源服务实例
video_source_service = VideoSourceService()
