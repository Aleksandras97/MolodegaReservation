from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class UserCreate(BaseModel):
    id: Optional[UUID] = None
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

class User(BaseModel):
    id: UUID
    name: str
    email: str

    class Config:
        orm_mode = True