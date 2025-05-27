from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from models.task import Task
from enums.task_enums import TaskPriority, TaskStatus
from .i_task_repository import ITaskRepository
import datetime

class SqlAlchemyTaskRepository(ITaskRepository):
    def __init__(self, db_session: Session):
        self.db = db_session

    def add_task(self, task_data: Dict[str, Any]) -> Task:
        db_task = Task(
            title=task_data.get("title"),
            description=task_data.get("description"),
            priority=task_data.get("priority"),
            due_date=task_data.get("due_date"),
            status=task_data.get("status")
        )
        if "created_at" in task_data and task_data["created_at"] is not None:
             db_task.created_at = task_data["created_at"]
        
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        return self.db.query(Task).filter(Task.id == task_id).first()

    def get_all_tasks(self, filters: Optional[Dict[str, Any]] = None, 
                      order_by_column: Optional[str] = "id", 
                      order_desc: bool = False) -> List[Task]:
        query = self.db.query(Task)
        
        if filters:
            for key, value in filters.items():
                if hasattr(Task, key):
                    column = getattr(Task, key)
                    if isinstance(value, list):
                         query = query.filter(column.in_(value))
                    else:
                         query = query.filter(column == value)

        if order_by_column and hasattr(Task, order_by_column):
            column_to_order = getattr(Task, order_by_column)
            if order_desc:
                query = query.order_by(column_to_order.desc())
            else:
                query = query.order_by(column_to_order.asc())
        else:
            query = query.order_by(Task.id.asc())

        return query.all()

    def update_task(self, task_id: int, update_data: Dict[str, Any]) -> Optional[Task]:
        db_task = self.get_task_by_id(task_id)
        if db_task:
            for key, value in update_data.items():
                if hasattr(db_task, key):
                    setattr(db_task, key, value)
            self.db.commit()
            self.db.refresh(db_task)
        return db_task

    def delete_task(self, task_id: int) -> bool:
        db_task = self.get_task_by_id(task_id)
        if db_task:
            self.db.delete(db_task)
            self.db.commit()
            return True
        return False