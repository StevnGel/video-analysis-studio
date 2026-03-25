import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Optional, Callable, Any
from src.config.config import settings


class ConcurrentManager:
    """并发管理器类"""
    
    _instance: Optional['ConcurrentManager'] = None
    _lock = threading.Lock()
    
    def __init__(self):
        """初始化并发管理器"""
        self.thread_pool = ThreadPoolExecutor(
            max_workers=settings.thread_pool_size,
            thread_name_prefix="video-analysis-"
        )
    
    @classmethod
    def get_instance(cls) -> 'ConcurrentManager':
        """获取并发管理器实例"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = ConcurrentManager()
        return cls._instance
    
    def submit_task(self, func: Callable, *args, **kwargs) -> Any:
        """提交任务到线程池
        
        Args:
            func: 要执行的函数
            *args: 函数参数
            **kwargs: 函数关键字参数
            
        Returns:
            Any: 任务执行结果
        """
        return self.thread_pool.submit(func, *args, **kwargs)
    
    def shutdown(self, wait: bool = True) -> None:
        """关闭线程池
        
        Args:
            wait: 是否等待所有任务完成
        """
        self.thread_pool.shutdown(wait=wait)


# 创建并发管理器实例
concurrent_manager = ConcurrentManager.get_instance()
