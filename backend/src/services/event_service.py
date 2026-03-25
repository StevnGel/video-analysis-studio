from typing import List, Optional
from src.schemas.event import Event, EventCreate, EventUpdate
from src.utils.supabase_client import supabase


class EventService:
    """事件服务类"""
    
    def __init__(self):
        """初始化事件服务"""
        self.table_name = "events"
    
    def create_event(self, event: EventCreate) -> Event:
        """创建事件
        
        Args:
            event: 事件创建模型
            
        Returns:
            Event: 创建的事件
        """
        # 转换为字典并插入数据
        data = event.model_dump()
        response = supabase.table(self.table_name).insert(data).execute()
        
        # 检查响应
        if response.data:
            return Event(**response.data[0])
        else:
            raise Exception("创建事件失败")
    
    def get_event(self, event_id: str) -> Optional[Event]:
        """获取事件
        
        Args:
            event_id: 事件ID
            
        Returns:
            Optional[Event]: 事件对象
        """
        response = supabase.table(self.table_name).select("*").eq("id", event_id).execute()
        
        if response.data:
            return Event(**response.data[0])
        else:
            return None
    
    def get_events(self, limit: int = 100, offset: int = 0) -> List[Event]:
        """获取事件列表
        
        Args:
            limit: 限制数量
            offset: 偏移量
            
        Returns:
            List[Event]: 事件列表
        """
        response = supabase.table(self.table_name).select("*").limit(limit).offset(offset).execute()
        
        if response.data:
            return [Event(**item) for item in response.data]
        else:
            return []
    
    def get_events_by_task(self, task_id: str, limit: int = 100, offset: int = 0) -> List[Event]:
        """根据任务获取事件列表
        
        Args:
            task_id: 任务ID
            limit: 限制数量
            offset: 偏移量
            
        Returns:
            List[Event]: 事件列表
        """
        response = supabase.table(self.table_name).select("*").eq("task_id", task_id).limit(limit).offset(offset).execute()
        
        if response.data:
            return [Event(**item) for item in response.data]
        else:
            return []
    
    def update_event(self, event_id: str, event: EventUpdate) -> Optional[Event]:
        """更新事件
        
        Args:
            event_id: 事件ID
            event: 事件更新模型
            
        Returns:
            Optional[Event]: 更新后的事件
        """
        # 转换为字典，排除None值
        data = event.model_dump(exclude_unset=True)
        response = supabase.table(self.table_name).update(data).eq("id", event_id).execute()
        
        if response.data:
            return Event(**response.data[0])
        else:
            return None
    
    def delete_event(self, event_id: str) -> bool:
        """删除事件
        
        Args:
            event_id: 事件ID
            
        Returns:
            bool: 是否删除成功
        """
        response = supabase.table(self.table_name).delete().eq("id", event_id).execute()
        return len(response.data) > 0


# 创建事件服务实例
event_service = EventService()
