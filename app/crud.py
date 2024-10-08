from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate
from hashlib import sha256
from uuid import UUID, uuid4

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    print(f"Request data: {user}")
    hashed_password = sha256(user.password.encode()).hexdigest()
    db_user = User(id=str(uuid4()), name=user.name, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.user_id == user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False

def update_user(db: Session, user_id: int, updated_user: UserCreate):
    db_user = db.query(User).filter(User.user_id == user_id)
    if db_user:
        db_user.name = updated_user.name
        db_user.email = updated_user.email
        db_user.hashed_password = sha256(updated_user.password.encode()).hexdigest()
        db.commit()
        db.refresh(db_user)
        return db_user
    return None