from sqlalchemy import Column, Integer, String, Date, Enum as SQLAlchemyEnum
import datetime
from core.database import Base
from enums.task_enums import TaskPriority, TaskStatus

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False, index=True)
    description = Column(String(255), nullable=True)
    
    priority = Column(SQLAlchemyEnum(TaskPriority), default=TaskPriority.MEDIUM, nullable=False)
    due_date = Column(Date, nullable=True)
    status = Column(SQLAlchemyEnum(TaskStatus), default=TaskStatus.TODO, nullable=False)
    
    created_at = Column(Date, default=datetime.date.today)

    def __repr__(self):
        return (f"<Task(id={self.id}, title='{self.title}', "
                f"priority='{self.priority.value}', status='{self.status.value}')>")