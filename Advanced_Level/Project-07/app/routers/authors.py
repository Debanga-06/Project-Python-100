from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/authors", tags=["Authors"])


@router.post("/", response_model=schemas.Author, status_code=status.HTTP_201_CREATED)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db, author)


@router.get("/", response_model=List[schemas.Author])
def list_authors(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return crud.get_authors(db, skip=skip, limit=limit)


@router.get("/{author_id}", response_model=schemas.AuthorWithBooks)
def get_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author(db, author_id)
    if not author:
        raise HTTPException(status_code=404, detail=f"Author with id {author_id} not found")
    return author


@router.put("/{author_id}", response_model=schemas.Author)
def update_author(author_id: int, updates: schemas.AuthorUpdate, db: Session = Depends(get_db)):
    author = crud.update_author(db, author_id, updates)
    if not author:
        raise HTTPException(status_code=404, detail=f"Author with id {author_id} not found")
    return author


@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_author(db, author_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Author with id {author_id} not found")
    return None
