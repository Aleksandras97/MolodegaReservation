import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/db_name"
# SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  
# Using SQLite for simplicity
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine("postgresql://fastapi_user:password123!@localhost/book_reservation_db")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()