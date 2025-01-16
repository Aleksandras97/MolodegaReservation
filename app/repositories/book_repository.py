from sqlalchemy.orm import Session
from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate

# create a new book
def create_book(db: Session, book: BookCreate):
    db_book = Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

# get book by id
def get_book_by_id(db: Session, book_id: int):
    return db.query(Book).filter(Book.id == book_id).first()

# get all books
def get_books(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Book).offset(skip).limit(limit).all()

def search_books(db: Session, search: str, page: int, size: int):
    query = db.query(Book)
    if search:
        query = query.filter(
            Book.title.ilike(f"%{search}%") |
            Book.author.ilike(f"%{search}%")
        )

    total = query.count()
    books = query.offset((page - 1) * size).limit(size).all()
    return books, total

# update an existing book
def update_book(db: Session, book_id: int, book_update: BookUpdate):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        return None
    
    updates = book_update.model_dump(exclude_unset=True)

    if "title" in updates:
        db_book.title = updates["title"]
    if "author" in updates:
        db_book.author = updates["author"]
    if "genre" in updates:
        db_book.genre = updates["genre"]
    if "isbn" in updates:
        db_book.isbn = updates["isbn"]
    if "status" in updates:
        db_book.status = updates["status"]
    if "publish_date" in updates:
        db_book.publish_date = updates["publish_date"]
    if "description" in updates:
        db_book.description = updates["description"]
    if "count" in updates:
        db_book.count = updates["count"]

    db.commit()
    db.refresh(db_book)
    return db_book

# delete a book
def delete_book(db: Session, book_id: int):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book:
        db.delete(db_book)
        db.commit()
    return db_book