from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from models.task import Task

class ITaskRepository(ABC):
    @abstractmethod
    def add_task(self, task_data: Dict[str, Any]) -> Task:
        pass

    @abstractmethod
    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        pass

    @abstractmethod
    def get_all_tasks(self, filters: Optional[Dict[str, Any]] = None, 
                      order_by_column: Optional[str] = "id", 
                      order_desc: bool = False) -> List[Task]:
        pass

    @abstractmethod
    def update_task(self, task_id: int, update_data: Dict[str, Any]) -> Optional[Task]:
        pass

    @abstractmethod
    def delete_task(self, task_id: int) -> bool:
        pass