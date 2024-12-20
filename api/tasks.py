import fastapi
from fastapi import Depends,HTTPException

from models.task import TaskCreate, Task, TaskUpdate
from models.user import User, UserCreate, UserLogin
from db import get_session
from sqlmodel import Session,select
from datetime import datetime
from auth import get_current_user

router = fastapi.APIRouter()

@router.get("/tasks")
async def get_tasks(session:Session = Depends(get_session)):
    statement = select(Task, User).join(User, Task.created_by == User.id)
    results = session.exec(statement).all()
    
    # Convert results to a list of dictionaries with task and creator info
    tasks = []
    for task, user in results:
        task_dict = task.model_dump()
        task_dict["creator"] = {
            "id": user.id,
            "username": user.username,
            # Add other user fields you want to include
        }
        tasks.append(task_dict)
    return tasks

@router.post("/tasks")
async def create_task(
    task_data: TaskCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    new_task = Task(
        title=task_data.title,
        description=task_data.description,
        completed=task_data.completed,
        created_by=current_user.id  # Automatically set created_by to current user's ID
    )
    
    session.add(new_task)
    session.commit()
    session.refresh(new_task)
    return new_task


@router.get("/tasks/{id}")
async def get_task(id:int,session:Session = Depends(get_session)):
    task = session.exec(select(Task).where(Task.id == id)).first()
    if not task:
        raise HTTPException(status_code=404,detail="Task not found")
    return task


@router.put("/tasks/{id}")
async def update_task(id: int, task_update: TaskUpdate, session: Session = Depends(get_session)):
    # First, get the existing task
    db_task = session.exec(select(Task).where(Task.id == id)).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Update task data
    task_data = task_update.model_dump(exclude_unset=True)
    for key, value in task_data.items():
        setattr(db_task, key, value)
    
    # # Update the updated_at timestamp
    db_task.updated_at = datetime.utcnow()
    
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@router.delete("/tasks/{id}")
async def delete_task(id:int,session:Session = Depends(get_session)):
    task = session.exec(select(Task).where(Task.id == id)).first()  
    if not task:
        raise HTTPException(status_code=404,detail="Task not found")
    session.delete(task)
    session.commit()
    return {"message":"Task deleted"}






