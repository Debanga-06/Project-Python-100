"""
Pydantic models - these are what actually validate incoming request bodies
and shape what gets sent back out. Kept "Create" schemas separate from the
full "Read" schemas since you don't want to require an id when creating
something, but you do want to return one.
"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


# ---------- Author schemas ----------

class AuthorBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=120, examples=["George Orwell"])
    country: Optional[str] = Field(None, max_length=80, examples=["United Kingdom"])


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=120)
    country: Optional[str] = Field(None, max_length=80)


class Author(AuthorBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class AuthorWithBooks(Author):
    books: List["Book"] = []


# ---------- Book schemas ----------

class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, examples=["1984"])
    genre: Optional[str] = Field(None, max_length=80, examples=["Dystopian"])
    price: float = Field(..., ge=0, examples=[12.99])
    published_year: Optional[int] = Field(None, ge=1400, le=2100, examples=[1949])


class BookCreate(BookBase):
    author_id: int


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    genre: Optional[str] = Field(None, max_length=80)
    price: Optional[float] = Field(None, ge=0)
    published_year: Optional[int] = Field(None, ge=1400, le=2100)
    author_id: Optional[int] = None


class Book(BookBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    author_id: int
    created_at: datetime


class BookWithAuthor(Book):
    author: Author


AuthorWithBooks.model_rebuild()
