from pydantic import BaseModel
from datetime import datetime

class ReservationBase(BaseModel):
    user_id: int
    book_id: int

class ReservationCreate(ReservationBase):
    pass

class ReservationResponse(ReservationBase):
    reserved_at: datetime
    expiration_at: datetime
    book_title: str
    book_author: str
    user_name: str

    class Config:
        from_attributes = True