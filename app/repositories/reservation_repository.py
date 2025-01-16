from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from app.models.reservation import Reservation
from app.models.book import Book
from app.models.user import User
from app.schemas.reservation import ReservationCreate, ReservationResponse


def create_reservation(db: Session, reservation: ReservationCreate):
    book = db.query(Book).filter(Book.id == reservation.book_id).first()
    if not book or book.status != "available":
        raise ValueError("Book is not available for reservation.")

    expiration_at = datetime.now() + timedelta(days=30)
    # Create a reservation
    db_reservation = Reservation(
        user_id=reservation.user_id,
        book_id=reservation.book_id,
        expiration_at=expiration_at,
    )
    db.add(db_reservation)

    # Update book status
    book.status = "reserved"
    db.commit()
    db.refresh(db_reservation)
    return get_reservation(db, db_reservation.id)


def get_reservation_by_user(db: Session, user_id: int):
    reservations = (
        db.query(Reservation)
        .join(Book, Reservation.book_id == Book.id)  # Join Book table
        .filter(Reservation.user_id == user_id)
        .all()
    )

    reservation_responses = [
        ReservationResponse(
            user_id=res.user_id,
            book_id=res.book_id,
            reserved_at=res.reserved_at,
            expiration_at=res.expiration_at,
            book_title=res.book.title,
            book_author=res.book.author,
            user_name=res.user.name
        )
        for res in reservations
    ]

    return reservation_responses


def get_reservation_by_book(db: Session, book_id: int):
    reservations = (
        db.query(Reservation)
        .join(User, Reservation.user_id == User.id)  # Join User table
        .filter(Reservation.book_id == book_id)
        .all()
    )

    reservation_responses = [
        ReservationResponse(
            user_id=res.user_id,
            book_id=res.book_id,
            reserved_at=res.reserved_at,
            expiration_at=res.expiration_at,
            book_title=res.book.title,
            book_author=res.book.author,
            user_name=res.user.name
        )
        for res in reservations
    ]

    return reservation_responses

def get_reservation(db: Session, reservation_id: int):
    reservation = (
        db.query(Reservation, Book.title.label("book_title"), Book.author.label("book_author"), User.name.label("user_name"))
        .join(Book, Reservation.book_id == Book.id)
        .join(User, Reservation.user_id == User.id)
        .filter(Reservation.id == reservation_id)
        .first()
    )

    if not reservation:
        return None

    reservation_data = reservation.Reservation
    return ReservationResponse(
        id=reservation_data.id,
        user_id=reservation_data.user_id,
        book_id=reservation_data.book_id,
        expiration_at=reservation_data.expiration_at,
        reserved_at=reservation_data.reserved_at,
        book_title=reservation.book_title,
        book_author=reservation.book_author,
        user_name=reservation.user_name,
    )