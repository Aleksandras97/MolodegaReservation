from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.reservation import ReservationCreate, ReservationResponse
from app.repositories import reservation_repository
from app.database import get_db

router = APIRouter()

@router.post('/', response_model=ReservationResponse)
def reserve_book(reservation: ReservationCreate, db: Session = Depends(get_db)):
    try:
        return reservation_repository.create_reservation(db, reservation)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/user/{user_id}", response_model=list[ReservationResponse])
def get_user_reservations(user_id: int, db:Session = Depends(get_db)):
    return reservation_repository.get_reservation_by_user(db, user_id)

@router.get("/book/{book_id}", response_model=list[ReservationResponse])
def get_user_reservations(book_id: int, db:Session = Depends(get_db)):
    return reservation_repository.get_reservation_by_book(db, book_id)