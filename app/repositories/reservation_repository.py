from sqlalchemy.orm import Session
from app.models.reservation import Reservation
from app.models.book import Book
from app.schemas.reservation import ReservationCreate

def create_reservation(db: Session, reservation: ReservationCreate):
    book = db.query(Book).filter(Book.id == reservation.book_id).first()
    if not book or book.status != "available":
        raise ValueError("Book is not available for reservation.")

    # Create a reservation
    db_reservation = Reservation(
        user_id=reservation.user_id,
        book_id=reservation.book_id,
        expiration_at=reservation.expiration_at
    )
    db.add(db_reservation)

    # Update book status
    book.status = "reserved"
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

def get_reservation_by_user(db: Session, user_id: int):
    return db.query(Reservation).filter(Reservation.user_id == user_id).all()

def get_reservation_by_book(db: Session, book_id: int):
    return db.query(Reservation).filter(Reservation.id == book_id).all()