from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.book import BookResponse, BookUpdate
from app.repositories import book_repository

router = APIRouter(prefix="/books", tags=["Books"])


@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book_id: int, db: Session = Depends(get_db)):
    book = book_repository.get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = book_repository.get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.get("/", response_model=list[BookResponse])
def get_books(
        search: str = "",
        page: int = Query(1, ge=1),
        size: int = Query(10, ge=1),
        db: Session = Depends(get_db)
):
    books, total = book_repository.search_books(db, search, page, size)
    return books


@router.put("/{book_id}", response_model=BookResponse)
def update_book_api(book_id: int, book_update: BookUpdate, db: Session = Depends(get_db)):
    updated_book = book_repository.update_book(db, book_id, book_update)
    if not updated_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book_api(book_id: int, db: Session = Depends(get_db)):
    book = book_repository.delete_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")