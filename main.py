# from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from app.core.config import settings
# from app.api.endpoints import todos
# from app.db.base import Base
# from app.db.session import engine

# # Create database tables
# Base.metadata.create_all(bind=engine)

# app = FastAPI(
#     title=settings.PROJECT_NAME,
#     openapi_url=f"{settings.API_V1_STR}/openapi.json"
# )



# # Include routers
# app.include_router(
#     todos.router,
#     prefix=f"{settings.API_V1_STR}/todos",
#     tags=["todos"]
# )

from fastapi import FastAPI
from db import init_db
from contextlib import asynccontextmanager
from api.tasks import router as tasks_router
from api.users import router as users_router
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="TODO API",
    version="1.0.0",
    description="API for managing TODO tasks",
    contact={
        "name": "Ryan Wong",
        "email": "chiayi520@gmail.com",
    },
    lifespan=lifespan
)

# # Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vue.js default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks_router)
app.include_router(users_router)
