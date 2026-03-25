from typing import List, Optional
from src.schemas.config import Config, ConfigCreate, ConfigUpdate
from src.utils.supabase_client import supabase


class ConfigService:
    """配置服务类"""
    
    def __init__(self):
        """初始化配置服务"""
        self.table_name = "configs"
    
    def create_config(self, config: ConfigCreate) -> Config:
        """创建配置
        
        Args:
            config: 配置创建模型
            
        Returns:
            Config: 创建的配置
        """
        # 转换为字典并插入数据
        data = config.model_dump()
        response = supabase.table(self.table_name).insert(data).execute()
        
        # 检查响应
        if response.data:
            return Config(**response.data[0])
        else:
            raise Exception("创建配置失败")
    
    def get_config(self, config_id: str) -> Optional[Config]:
        """获取配置
        
        Args:
            config_id: 配置ID
            
        Returns:
            Optional[Config]: 配置对象
        """
        response = supabase.table(self.table_name).select("*").eq("id", config_id).execute()
        
        if response.data:
            return Config(**response.data[0])
        else:
            return None
    
    def get_config_by_key(self, key: str) -> Optional[Config]:
        """根据键获取配置
        
        Args:
            key: 配置键
            
        Returns:
            Optional[Config]: 配置对象
        """
        response = supabase.table(self.table_name).select("*").eq("key", key).execute()
        
        if response.data:
            return Config(**response.data[0])
        else:
            return None
    
    def get_configs(self, limit: int = 100, offset: int = 0) -> List[Config]:
        """获取配置列表
        
        Args:
            limit: 限制数量
            offset: 偏移量
            
        Returns:
            List[Config]: 配置列表
        """
        response = supabase.table(self.table_name).select("*").limit(limit).offset(offset).execute()
        
        if response.data:
            return [Config(**item) for item in response.data]
        else:
            return []
    
    def get_configs_by_category(self, category: str, limit: int = 100, offset: int = 0) -> List[Config]:
        """根据分类获取配置列表
        
        Args:
            category: 配置分类
            limit: 限制数量
            offset: 偏移量
            
        Returns:
            List[Config]: 配置列表
        """
        response = supabase.table(self.table_name).select("*").eq("category", category).limit(limit).offset(offset).execute()
        
        if response.data:
            return [Config(**item) for item in response.data]
        else:
            return []
    
    def update_config(self, config_id: str, config: ConfigUpdate) -> Optional[Config]:
        """更新配置
        
        Args:
            config_id: 配置ID
            config: 配置更新模型
            
        Returns:
            Optional[Config]: 更新后的配置
        """
        # 转换为字典，排除None值
        data = config.model_dump(exclude_unset=True)
        response = supabase.table(self.table_name).update(data).eq("id", config_id).execute()
        
        if response.data:
            return Config(**response.data[0])
        else:
            return None
    
    def update_config_by_key(self, key: str, config: ConfigUpdate) -> Optional[Config]:
        """根据键更新配置
        
        Args:
            key: 配置键
            config: 配置更新模型
            
        Returns:
            Optional[Config]: 更新后的配置
        """
        # 转换为字典，排除None值
        data = config.model_dump(exclude_unset=True)
        response = supabase.table(self.table_name).update(data).eq("key", key).execute()
        
        if response.data:
            return Config(**response.data[0])
        else:
            return None
    
    def delete_config(self, config_id: str) -> bool:
        """删除配置
        
        Args:
            config_id: 配置ID
            
        Returns:
            bool: 是否删除成功
        """
        response = supabase.table(self.table_name).delete().eq("id", config_id).execute()
        return len(response.data) > 0


# 创建配置服务实例
config_service = ConfigService()
