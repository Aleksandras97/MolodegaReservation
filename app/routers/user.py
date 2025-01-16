from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories import user_repository
from app.schemas import user

router = APIRouter(prefix="/users", tags=["users"])

@router.post('/', response_model=user.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: user.UserCreate, db: Session = Depends(get_db)):
    db_user = user_repository.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_repository.create_user(db, user)

@router.get("/{user_id}", response_model=user.User)
def read_user(user_id: str, db: Session = Depends(get_db)):
    db_user = user_repository.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/", response_model=list[user.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = user_repository.get_users(db, skip=skip, limit=limit)
    return users


@router.put("/{user_id}", response_model=user.User)
def update_user(user_id: str, user: user.UserCreate, db: Session = Depends(get_db)):
    updated_user = user_repository.update_user(db, user_id, user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str, db: Session = Depends(get_db)):
    success = user_repository.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted"}