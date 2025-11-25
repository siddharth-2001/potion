from pydantic import BaseModel, EmailStr, ConfigDict
import uuid


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    
class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: uuid.UUID
    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: EmailStr
    password: str