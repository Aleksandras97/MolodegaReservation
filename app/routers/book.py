from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.book import BookCreate, BookResponse, BookUpdate
from app.repositories.book_repository import create_book, get_book, get_books, update_book, delete_book

router = APIRouter(prefix="/books", tags=["Books"])


@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book_api(book_id: int, db: Session = Depends(get_db)):
    book = get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.get("/{book_id}", response_model=BookResponse)
def get_book_api(book_id: int, db: Session = Depends(get_db)):
    book = get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.get("/", response_model=list[BookResponse])
def get_books_api(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_books(db, skip, limit)

@router.put("/{book_id}", response_model=BookResponse)
def update_book_api(book_id: int, book_update: BookUpdate, db: Session = Depends(get_db)):
    updated_book = update_book(db, book_id, book_update)
    if not update_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return update_book

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book_api(book_id: int, db: Session = Depends(get_db)):
    book = delete_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")