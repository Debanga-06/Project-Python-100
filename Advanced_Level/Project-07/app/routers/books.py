from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/books", tags=["Books"])


@router.post("/", response_model=schemas.Book, status_code=status.HTTP_201_CREATED)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    created = crud.create_book(db, book)
    if not created:
        raise HTTPException(
            status_code=400,
            detail=f"author_id {book.author_id} does not exist - create the author first",
        )
    return created


@router.get("/", response_model=List[schemas.Book])
def list_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    genre: Optional[str] = Query(None, description="Filter by genre (partial match)"),
    author_id: Optional[int] = Query(None, description="Filter by author id"),
    search: Optional[str] = Query(None, description="Search by title (partial match)"),
    db: Session = Depends(get_db),
):
    return crud.get_books(db, skip=skip, limit=limit, genre=genre, author_id=author_id, search=search)


@router.get("/{book_id}", response_model=schemas.BookWithAuthor)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")
    return book


@router.put("/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, updates: schemas.BookUpdate, db: Session = Depends(get_db)):
    try:
        book = crud.update_book(db, book_id, updates)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not book:
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")
    return book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_book(db, book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")
    return None
