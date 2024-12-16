from typing import List, Optional
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship,MetaData


class UserBase(SQLModel):
    username: str
    email: str
    hashed_password: str

class User(UserBase, table=True):
    __table_args__ = {'schema': 'todo_app'}
    id: Optional[int] = Field(default=None, primary_key=True)
    tasks: List["Task"] = Relationship(back_populates="creator")

class UserCreate(SQLModel):
    username: str
    email: str
    password: str  # Plain password for creation only

class UserLogin(SQLModel):
    email: str
    password: str