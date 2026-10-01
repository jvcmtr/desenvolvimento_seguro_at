from sqlmodel import SQLModel, create_engine, Session
from app.config import settings

connect_args = {"check_same_thread": False} if "sqlite" in settings.TARGET_DATABASE_URL else {}
engine = create_engine(settings.TARGET_DATABASE_URL, echo=True, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session() -> Session:
    with Session(engine) as session:
        yield session