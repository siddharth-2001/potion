from pydantic import BaseModel, EmailStr, ConfigDict
import uuid
from typing import Optional


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    
class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: uuid.UUID
    token: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserTokenModel(BaseModel):
    message: Optional[str] = None
    token: str

class CommonHeaders(BaseModel):
    authorization: str

class UserChangePassword(UserLogin):
    new_password: str
