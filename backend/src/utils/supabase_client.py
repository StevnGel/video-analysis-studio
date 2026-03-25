from supabase import create_client, Client
from src.config.config import settings


class SupabaseClient:
    """Supabase 客户端管理类"""
    
    _instance: Optional[Client] = None
    
    @classmethod
    def get_instance(cls) -> Client:
        """获取 Supabase 客户端实例"""
        if cls._instance is None:
            cls._instance = create_client(
                settings.supabase_url,
                settings.supabase_key
            )
        return cls._instance


# 创建 Supabase 客户端实例
supabase = SupabaseClient.get_instance()
