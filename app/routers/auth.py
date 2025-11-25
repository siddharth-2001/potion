from argon2 import PasswordHasher
from fastapi import APIRouter, Depends

from app.schemas.user import UserCreate, UserRead, UserLogin
from app.repositories.user_repository import UserRepository
from app.dependencies import get_user_repository, get_password_hasher


auth_router = APIRouter()


@auth_router.post("/register")
def register_user(
    user: UserCreate,
    user_repo: UserRepository = Depends(get_user_repository),
    hasher: PasswordHasher = Depends(get_password_hasher),
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
):
    user = user_repo.get_user_by_email(credentials.email)

    if user is None:
        raise ValueError("User not found")

    out_user = UserRead.model_validate(user) if user else None
    if hasher.verify(user.hashed_password, credentials.password):
        return out_user
    return {"message": "Invalid credentials"}
