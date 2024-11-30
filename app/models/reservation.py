from http.cookiejar import UTC_ZONES

from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id", nullable=False))
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    reserved_at = Column(DateTime, default=datetime.now(tz=UTC_ZONES))
    expiration_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="reservations")
    book = relationship("Book", back_populates="reservations")