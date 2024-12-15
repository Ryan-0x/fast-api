from typing import List, Optional
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship,MetaData


class UserBase(SQLModel):
    username: str
    email: str
    password: str

class User(UserBase, table=True):
    __table_args__ = {'schema': 'todo_app'}
    id: Optional[int] = Field(default=None, primary_key=True)
    tasks: List["Task"] = Relationship(back_populates="creator")

class TaskBase(SQLModel):
    title: str
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)

class Task(TaskBase, table=True):
    __table_args__ = {'schema': 'todo_app'}
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: int = Field(foreign_key="todo_app.user.id")
    creator: User = Relationship(back_populates="tasks")  

class TaskCreate(TaskBase):
    created_by: int  # Required user ID when creating a task

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
