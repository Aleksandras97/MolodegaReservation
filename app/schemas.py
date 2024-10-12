from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

class User(BaseModel):
    id: str
    name: Optional[str] = None
    email: Optional[str] = None

    class Config:
        orm_mode = True