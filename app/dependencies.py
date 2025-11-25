from functools import lru_cache
from fastapi import Depends
from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.database import get_db_session
from argon2 import PasswordHasher

def get_user_repository(session: Session = Depends(get_db_session)) -> UserRepository:
    return UserRepository(session)

@lru_cache()
def get_password_hasher() -> PasswordHasher:
    return PasswordHasher()