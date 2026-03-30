from typing import Optional, Any
from src.config.config import settings


class MockSupabaseClient:
    """模拟 Supabase 客户端类"""
    
    def table(self, table_name: str):
        """模拟 table 方法"""
        return MockTable()
    
    def auth(self):
        """模拟 auth 方法"""
        return MockAuth()


class MockTable:
    """模拟 Table 类"""
    
    def select(self, *args, **kwargs):
        """模拟 select 方法"""
        return self
    
    def insert(self, *args, **kwargs):
        """模拟 insert 方法"""
        return self
    
    def update(self, *args, **kwargs):
        """模拟 update 方法"""
        return self
    
    def delete(self, *args, **kwargs):
        """模拟 delete 方法"""
        return self
    
    def eq(self, *args, **kwargs):
        """模拟 eq 方法"""
        return self
    
    def limit(self, *args, **kwargs):
        """模拟 limit 方法"""
        return self
    
    def execute(self):
        """模拟 execute 方法"""
        return {"data": [], "error": None}


class MockAuth:
    """模拟 Auth 类"""
    
    def sign_in(self, *args, **kwargs):
        """模拟 sign_in 方法"""
        return {"data": None, "error": None}
    
    def sign_out(self):
        """模拟 sign_out 方法"""
        return {"data": None, "error": None}


class SupabaseClient:
    """Supabase 客户端管理类"""
    
    _instance: Optional[MockSupabaseClient] = None
    
    @classmethod
    def get_instance(cls) -> MockSupabaseClient:
        """获取 Supabase 客户端实例"""
        if cls._instance is None:
            cls._instance = MockSupabaseClient()
        return cls._instance


# 创建 Supabase 客户端实例
supabase = SupabaseClient.get_instance()
