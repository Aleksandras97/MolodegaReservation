from sqlalchemy import Column, Integer, String, Date, Enum
from sqlalchemy.orm import relationship
from app.database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    isbn = Column(String, unique=True, nullable=False)
    publish_date = Column(Date, nullable=False)
    status = Column(String, nullable=True)
    description = Column(String, nullable=True)
    count = Column(Integer, nullable=False)

    reservations = relationship("Reservation", back_populates="book")