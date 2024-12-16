from typing import List, Optional
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship,MetaData


class TaskBase(SQLModel):
    title: str
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)

class Task(TaskBase, table=True):
    __table_args__ = {'schema': 'todo_app'}
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    created_by: int = Field(foreign_key="todo_app.user.id")
    creator: "User" = Relationship(back_populates="tasks")  

class TaskCreate(TaskBase):
    pass

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


