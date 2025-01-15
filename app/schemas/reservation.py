from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ReservationBase(BaseModel):
    user_id: int
    book_id: int
    expiration_at: Optional[datetime] = None

class ReservationCreate(ReservationBase):
    pass

class ReservationResponse(ReservationBase):
    int: int
    reserved_at: datetime

    class Config:
        from_attributes = True