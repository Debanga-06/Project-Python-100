"""
Run with:
    uvicorn app.main:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routers import authors, books

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Library API",
    description="A small RESTful API for managing authors and books - built as a CRUD/Flask-FastAPI practice project.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(authors.router)
app.include_router(books.router)


@app.get("/", tags=["Health"])
def root():
    return {"message": "Library API is running. Head to /docs for the interactive API docs."}


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}
