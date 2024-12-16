import fastapi
from fastapi import Depends,HTTPException,status
from models.user import User, UserCreate, UserLogin
from db import get_session
from sqlmodel import Session,select
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from auth import (
    verify_password, 
    get_password_hash, 
    create_access_token, 
    ACCESS_TOKEN_EXPIRE_MINUTES
)

router = fastapi.APIRouter()

@router.get("/users")
async def get_users(session:Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users

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

@router.post("/register")
async def register_user(user: UserCreate, session: Session = Depends(get_session)):
    # Check if user already exists
    db_user = session.exec(
        select(User).where(User.email == user.email)
    ).first()
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # Create new user with hashed password
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    # Find user by email
    user = session.exec(
        select(User).where(User.email == form_data.username)
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify password
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }