from typing import List, Optional
from src.schemas.model import Model, ModelCreate, ModelUpdate
from src.utils.supabase_client import supabase


class ModelService:
    """模型服务类"""
    
    def __init__(self):
        """初始化模型服务"""
        self.table_name = "models"
    
    def create_model(self, model: ModelCreate) -> Model:
        """创建模型
        
        Args:
            model: 模型创建模型
            
        Returns:
            Model: 创建的模型
        """
        # 转换为字典并插入数据
        data = model.model_dump()
        response = supabase.table(self.table_name).insert(data).execute()
        
        # 检查响应
        if response.data:
            return Model(**response.data[0])
        else:
            raise Exception("创建模型失败")
    
    def get_model(self, model_id: str) -> Optional[Model]:
        """获取模型
        
        Args:
            model_id: 模型ID
            
        Returns:
            Optional[Model]: 模型对象
        """
        response = supabase.table(self.table_name).select("*").eq("id", model_id).execute()
        
        if response.data:
            return Model(**response.data[0])
        else:
            return None
    
    def get_models(self, limit: int = 100, offset: int = 0) -> List[Model]:
        """获取模型列表
        
        Args:
            limit: 限制数量
            offset: 偏移量
            
        Returns:
            List[Model]: 模型列表
        """
        response = supabase.table(self.table_name).select("*").limit(limit).offset(offset).execute()
        
        if response.data:
            return [Model(**item) for item in response.data]
        else:
            return []
    
    def update_model(self, model_id: str, model: ModelUpdate) -> Optional[Model]:
        """更新模型
        
        Args:
            model_id: 模型ID
            model: 模型更新模型
            
        Returns:
            Optional[Model]: 更新后的模型
        """
        # 转换为字典，排除None值
        data = model.model_dump(exclude_unset=True)
        response = supabase.table(self.table_name).update(data).eq("id", model_id).execute()
        
        if response.data:
            return Model(**response.data[0])
        else:
            return None
    
    def delete_model(self, model_id: str) -> bool:
        """删除模型
        
        Args:
            model_id: 模型ID
            
        Returns:
            bool: 是否删除成功
        """
        response = supabase.table(self.table_name).delete().eq("id", model_id).execute()
        return len(response.data) > 0


# 创建模型服务实例
model_service = ModelService()
