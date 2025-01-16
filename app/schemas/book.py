from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

# Schema for creating a new book
class BookCreate(BaseModel):
    title: str
    author: str
    genre: str
    isbn: str
    status: Optional[str] = None
    publish_date: Optional[date] = None
    description: Optional[str] = None
    count: int = Field(..., ge=1) # Must have at least 1 book

# Schema for updating an existing book
class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    genre: Optional[str] = None
    isbn: Optional[str] = None
    status: Optional[str] = None
    publish_date: Optional[date] = None
    description: Optional[str] = None
    count: Optional[int] = None

class BookResponse(BookCreate):
    id: int
    title: str
    author: str

    class Config:
        from_attributes = True