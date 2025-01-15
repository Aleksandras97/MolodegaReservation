from sqlalchemy import create_engine
from database import Base

SQLALCHEMY_DATABASE_URL = "postgresql://fastapi_user:password123!@localhost/book_reservation_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

def reset_database():
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("Recreating all tables...")
    # Base.metadata.create_all(bind=engine)
    print("Database reset completed.")

if __name__ == "__main__":
    reset_database()