from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import get_settings

settings = get_settings()

engine = create_engine(settings.database_url, echo=True)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_session():
    session_instance = Session()
    try:
        yield session_instance
    finally:
        session_instance.close()
