import fastapi
from fastapi import Depends,HTTPException
from models import User
from db import get_session
from sqlmodel import Session,select



router = fastapi.APIRouter()

@router.get("/users")
async def get_users(session:Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users

@router.post("/users")
async def create_user(user:User,session:Session = Depends(get_session)):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.get("/users/{id}")
async def get_user(id:int,session:Session = Depends(get_session)):
    user = session.exec(select(User).where(User.id == id)).first()
    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    return user

@router.put("/users/{id}")
async def update_user(id:int,user:User,session:Session = Depends(get_session)):
    session.exec(select(User).where(User.id == id)).update(user)
    session.commit()
    return user

@router.delete("/users/{id}")
async def delete_user(id: int, session: Session = Depends(get_session)):
    # First, find the user
    user = session.exec(select(User).where(User.id == id)).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Delete the user
    session.delete(user)
    session.commit()
    
    return {"message": "User deleted"}
