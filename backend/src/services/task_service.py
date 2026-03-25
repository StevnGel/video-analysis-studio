from typing import List, Optional
from datetime import datetime
from src.schemas.task import Task, TaskCreate, TaskUpdate
from src.utils.supabase_client import supabase


class TaskService:
    """任务服务类"""
    
    def __init__(self):
        """初始化任务服务"""
        self.table_name = "tasks"
    
    def create_task(self, task: TaskCreate) -> Task:
        """创建任务
        
        Args:
            task: 任务创建模型
            
        Returns:
            Task: 创建的任务
        """
        # 转换为字典并插入数据
        data = task.model_dump()
        response = supabase.table(self.table_name).insert(data).execute()
        
        # 检查响应
        if response.data:
            return Task(**response.data[0])
        else:
            raise Exception("创建任务失败")
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """获取任务
        
        Args:
            task_id: 任务ID
            
        Returns:
            Optional[Task]: 任务对象
        """
        response = supabase.table(self.table_name).select("*").eq("id", task_id).execute()
        
        if response.data:
            return Task(**response.data[0])
        else:
            return None
    
    def get_tasks(self, limit: int = 100, offset: int = 0) -> List[Task]:
        """获取任务列表
        
        Args:
            limit: 限制数量
            offset: 偏移量
            
        Returns:
            List[Task]: 任务列表
        """
        response = supabase.table(self.table_name).select("*").limit(limit).offset(offset).execute()
        
        if response.data:
            return [Task(**item) for item in response.data]
        else:
            return []
    
    def update_task(self, task_id: str, task: TaskUpdate) -> Optional[Task]:
        """更新任务
        
        Args:
            task_id: 任务ID
            task: 任务更新模型
            
        Returns:
            Optional[Task]: 更新后的任务
        """
        # 转换为字典，排除None值
        data = task.model_dump(exclude_unset=True)
        
        # 如果状态变为running，设置开始时间
        if data.get("status") == "running":
            data["started_at"] = datetime.utcnow()
        # 如果状态变为completed，设置完成时间
        elif data.get("status") == "completed":
            data["completed_at"] = datetime.utcnow()
        
        response = supabase.table(self.table_name).update(data).eq("id", task_id).execute()
        
        if response.data:
            return Task(**response.data[0])
        else:
            return None
    
    def delete_task(self, task_id: str) -> bool:
        """删除任务
        
        Args:
            task_id: 任务ID
            
        Returns:
            bool: 是否删除成功
        """
        response = supabase.table(self.table_name).delete().eq("id", task_id).execute()
        return len(response.data) > 0


# 创建任务服务实例
task_service = TaskService()
