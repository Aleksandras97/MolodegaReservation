from sqlalchemy import Column, String
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True, default=None)
    email = Column(String, unique=True, index=True, default=None)
    hashed_password = Column(String, default=None)