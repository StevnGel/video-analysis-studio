import gi
import threading
from typing import Optional, Dict, Any

# 初始化 GStreamer
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject

Gst.init(None)


class GStreamerManager:
    """GStreamer 管理器类"""
    
    def __init__(self):
        """初始化 GStreamer 管理器"""
        self.pipelines: Dict[str, Gst.Pipeline] = {}
        self.pipeline_lock = threading.Lock()
    
    def create_pipeline(self, pipeline_id: str, pipeline_description: str) -> bool:
        """创建 GStreamer 管道
        
        Args:
            pipeline_id: 管道 ID
            pipeline_description: 管道描述字符串
            
        Returns:
            bool: 是否创建成功
        """
        try:
            with self.pipeline_lock:
                # 检查管道是否已存在
                if pipeline_id in self.pipelines:
                    return False
                
                # 创建管道
                pipeline = Gst.parse_launch(pipeline_description)
                self.pipelines[pipeline_id] = pipeline
                return True
        except Exception as e:
            print(f"创建管道失败: {e}")
            return False
    
    def start_pipeline(self, pipeline_id: str) -> bool:
        """启动 GStreamer 管道
        
        Args:
            pipeline_id: 管道 ID
            
        Returns:
            bool: 是否启动成功
        """
        try:
            with self.pipeline_lock:
                if pipeline_id not in self.pipelines:
                    return False
                
                pipeline = self.pipelines[pipeline_id]
                result = pipeline.set_state(Gst.State.PLAYING)
                return result == Gst.StateChangeReturn.SUCCESS
        except Exception as e:
            print(f"启动管道失败: {e}")
            return False
    
    def stop_pipeline(self, pipeline_id: str) -> bool:
        """停止 GStreamer 管道
        
        Args:
            pipeline_id: 管道 ID
            
        Returns:
            bool: 是否停止成功
        """
        try:
            with self.pipeline_lock:
                if pipeline_id not in self.pipelines:
                    return False
                
                pipeline = self.pipelines[pipeline_id]
                result = pipeline.set_state(Gst.State.NULL)
                return result == Gst.StateChangeReturn.SUCCESS
        except Exception as e:
            print(f"停止管道失败: {e}")
            return False
    
    def delete_pipeline(self, pipeline_id: str) -> bool:
        """删除 GStreamer 管道
        
        Args:
            pipeline_id: 管道 ID
            
        Returns:
            bool: 是否删除成功
        """
        try:
            with self.pipeline_lock:
                if pipeline_id not in self.pipelines:
                    return False
                
                # 先停止管道
                self.stop_pipeline(pipeline_id)
                
                # 删除管道
                del self.pipelines[pipeline_id]
                return True
        except Exception as e:
            print(f"删除管道失败: {e}")
            return False
    
    def get_pipeline_state(self, pipeline_id: str) -> Optional[Gst.State]:
        """获取管道状态
        
        Args:
            pipeline_id: 管道 ID
            
        Returns:
            Optional[Gst.State]: 管道状态
        """
        try:
            with self.pipeline_lock:
                if pipeline_id not in self.pipelines:
                    return None
                
                pipeline = self.pipelines[pipeline_id]
                _, state, _ = pipeline.get_state(0)
                return state
        except Exception as e:
            print(f"获取管道状态失败: {e}")
            return None
    
    def create_mp4_http_to_rtmp_pipeline(self, pipeline_id: str, http_url: str, rtmp_url: str) -> bool:
        """创建 MP4 HTTP 到 RTMP 的转流管道
        
        Args:
            pipeline_id: 管道 ID
            http_url: HTTP MP4 文件地址
            rtmp_url: RTMP 目标地址
            
        Returns:
            bool: 是否创建成功
        """
        # 构建 GStreamer 管道描述
        pipeline_description = f"""
            souphttpsrc location={http_url} is-live=false ! 
            decodebin ! 
            videoconvert ! 
            x264enc speed-preset=ultrafast tune=zerolatency ! 
            queue ! 
            mux. 
            decodebin. ! 
            audioconvert ! 
            lamemp3enc ! 
            queue ! 
            mux. 
            flvmux name=mux ! 
            rtmpsink location={rtmp_url}
        """
        
        # 调用创建管道方法
        return self.create_pipeline(pipeline_id, pipeline_description)


# 创建 GStreamer 管理器实例
gstreamer_manager = GStreamerManager()
