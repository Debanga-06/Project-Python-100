from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app import models, schemas


# ---------- Author CRUD ----------

def get_author(db: Session, author_id: int) -> Optional[models.Author]:
    return db.query(models.Author).filter(models.Author.id == author_id).first()


def get_authors(db: Session, skip: int = 0, limit: int = 20) -> List[models.Author]:
    return db.query(models.Author).offset(skip).limit(limit).all()


def create_author(db: Session, author: schemas.AuthorCreate) -> models.Author:
    db_author = models.Author(**author.model_dump())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def update_author(db: Session, author_id: int, updates: schemas.AuthorUpdate) -> Optional[models.Author]:
    db_author = get_author(db, author_id)
    if not db_author:
        return None
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(db_author, field, value)
    db.commit()
    db.refresh(db_author)
    return db_author


def delete_author(db: Session, author_id: int) -> bool:
    db_author = get_author(db, author_id)
    if not db_author:
        return False
    db.delete(db_author)
    db.commit()
    return True


# ---------- Book CRUD ----------

def get_book(db: Session, book_id: int) -> Optional[models.Book]:
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def get_books(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    genre: Optional[str] = None,
    author_id: Optional[int] = None,
    search: Optional[str] = None,
) -> List[models.Book]:
    query = db.query(models.Book)

    if genre:
        query = query.filter(models.Book.genre.ilike(f"%{genre}%"))
    if author_id:
        query = query.filter(models.Book.author_id == author_id)
    if search:
        query = query.filter(or_(models.Book.title.ilike(f"%{search}%")))

    return query.offset(skip).limit(limit).all()


def create_book(db: Session, book: schemas.BookCreate) -> Optional[models.Book]:
    author = get_author(db, book.author_id)
    if not author:
        return None
    db_book = models.Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def update_book(db: Session, book_id: int, updates: schemas.BookUpdate) -> Optional[models.Book]:
    db_book = get_book(db, book_id)
    if not db_book:
        return None

    update_data = updates.model_dump(exclude_unset=True)

    if "author_id" in update_data:
        author = get_author(db, update_data["author_id"])
        if not author:
            raise ValueError("author_id does not exist")

    for field, value in update_data.items():
        setattr(db_book, field, value)

    db.commit()
    db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int) -> bool:
    db_book = get_book(db, book_id)
    if not db_book:
        return False
    db.delete(db_book)
    db.commit()
    return True
