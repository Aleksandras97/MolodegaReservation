from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserResponse(BaseModel):
    id: str
    name: str
    email: Optional[EmailStr] = None

    class Config:
        from_attributes = True

class User(BaseModel):
    id: str
    name: Optional[str] = None
    email: Optional[EmailStr] = None

    class Config:
        from_attributes = True