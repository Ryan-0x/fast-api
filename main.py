from fastapi.middleware.cors import CORSMiddleware
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

# Include routers with prefix
app.include_router(
    tasks_router,
    prefix="/api/v1",
    tags=["tasks"]
)

app.include_router(
    users_router,
    prefix="/api/v1",
    tags=["users"]
)