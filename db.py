from sqlmodel import Session, SQLModel, create_engine ,text
import os
from dotenv import load_dotenv



load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://basfAdmin:BaSfAdm1n-!xx@postgres:5433/postgres")
engine = create_engine(DATABASE_URL,echo=True)

def init_db():
    with Session(engine) as session:
        # Create schema using raw SQL
        session.exec(text("CREATE SCHEMA IF NOT EXISTS todo_app"))
        session.commit()
        
        # Set schema and create tables
        SQLModel.metadata.create_all(bind=engine)

def get_session():
    with Session(engine) as session:
        yield session
