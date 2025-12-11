from argon2 import PasswordHasher
from fastapi import APIRouter, Depends, Header, HTTPException
from redis import Redis

from app.schemas.user import (
    UserCreate,
    UserRead,
    UserLogin,
    UserTokenModel,
    UserChangePassword,
)
from app.repositories.user_repository import UserRepository
from app.dependencies import (
    get_redis_client,
    get_user_repository,
    get_password_hasher,
    get_jwt_utils,
    get_current_user,
    get_auth_retry_service,
)
from app.core.security import JWTUtils
from app.models import User
from app.services.auth_retry import AuthRetryService

auth_router = APIRouter()

@auth_router.post("/register")
def register_user(
    user: UserCreate,
    user_repo: UserRepository = Depends(get_user_repository),
    hasher: PasswordHasher = Depends(get_password_hasher),
    redis: Redis = Depends(get_redis_client),
):
    hashed_password = hasher.hash(user.password)

    created_user = user_repo.create_user(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        hashed_password=hashed_password,
    )

    return UserRead.model_validate(created_user)


@auth_router.post("/login")
def login_user(
    credentials: UserLogin,
    user_repo: UserRepository = Depends(get_user_repository),
    hasher: PasswordHasher = Depends(get_password_hasher),
    jwt_utils: JWTUtils = Depends(get_jwt_utils),
    retry_service: AuthRetryService = Depends(get_auth_retry_service),
):
    user = user_repo.get_user_by_email(credentials.email)

    if user is None:
        raise HTTPException(status_code=401, detail="Incorrect email or password.")

    token = jwt_utils.encode(user_id=user.id, email=user.email)

    try:
        hasher.verify(user.hashed_password, credentials.password)
        return UserTokenModel(token=token, message="Login successful!")

    except:
        retry_service.increment_retry_count(str(user.id))
        raise HTTPException(status_code=401, detail="Incorrect email or password.")


@auth_router.get("/me")
def fetch_user(user: User = Depends(get_current_user)):

    response = UserRead.model_validate(user)
    return {"message": "User fetched successfully!", "details": response}


@auth_router.post("/change-password")
def change_password(
    data: UserChangePassword,
    user: User = Depends(get_current_user),
    hasher: PasswordHasher = Depends(get_password_hasher),
    user_repo: UserRepository = Depends(get_user_repository),
):
    if not hasher.verify(user.hashed_password, data.password):
        return {"message": "Incorrect User Password"}

    new_hashed_password = hasher.hash(data.new_password)
    user_repo.change_password(user, new_hashed_password)

    return {"message": "Password Changed successfully!"}
