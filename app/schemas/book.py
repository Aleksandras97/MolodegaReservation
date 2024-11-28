from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

# Schema for creating a new book
class BookCreate(BaseModel):
    title: str
    author: str
    genre: str
    isbn: str
    publish_date: Optional[date] = None
    description: Optional[str] = None
    count: int = Field(..., ge=1) # Must have at least 1 book

# Schema for updating an existing book
class BookUpdate(BaseModel):
    title: Optional[str]
    author: Optional[str]
    genre: Optional[str]
    isbn: Optional[str]
    publish_date: Optional[date]
    description: Optional[str]
    count: Optional[int]

class BookResponse(BookCreate):
    id: int
    status: str

    class Config:
        orm_mode = True