from functools import lru_cache
from fastapi import Depends, Header, HTTPException
from redis import Redis
from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.database import get_db_session
from argon2 import PasswordHasher
from app.core.security import JWTUtils
from app.core.config import get_settings
from app.models import User
from app.services.auth_retry import AuthRetryService


@lru_cache
def get_redis_client():
    settings = get_settings()
    return Redis(
        host=settings.redis_host, port=settings.redis_port, decode_responses=True
    )

@lru_cache
def get_auth_retry_service():
    return AuthRetryService(get_redis_client())

def get_user_repository(session: Session = Depends(get_db_session)) -> UserRepository:
    return UserRepository(session)


@lru_cache()
def get_password_hasher() -> PasswordHasher:
    return PasswordHasher()


@lru_cache()
def get_jwt_utils() -> JWTUtils:
    settings = get_settings()
    return JWTUtils(settings.jwt_secret_key)


def get_current_user(
    bearer: str = Header(alias="Authorization"),
    user_repo: UserRepository = Depends(get_user_repository),
    jwt_utils: JWTUtils = Depends(get_jwt_utils),
) -> User:
    token = jwt_utils.extract_token(bearer)
    payload = jwt_utils.decode(token)

    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(status_code=400, detail="Payload is missing user id.")

    user_match = user_repo.get_user_by_id(user_id)

    if user_match is None:
        raise HTTPException(status_code=404, detail="User not found.")

    return user_match
