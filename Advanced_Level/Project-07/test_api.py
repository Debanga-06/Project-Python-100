"""
Not a full pytest suite, just a quick script that hits every endpoint in
order (create author -> create book -> read -> update -> filter ->
delete) so you can see the whole CRUD cycle working end to end. Uses
FastAPI's TestClient so it doesn't need the server actually running.

    python test_api.py
"""

import os

# use a throwaway test db so this doesn't touch library.db
os.environ["DATABASE_URL"] = "sqlite:///./test_library.db"

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def check(condition, message):
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {message}")
    assert condition, message


def run():
    print("Creating an author...")
    resp = client.post("/authors/", json={"name": "George Orwell", "country": "United Kingdom"})
    check(resp.status_code == 201, "author creation returns 201")
    author = resp.json()
    author_id = author["id"]

    print("\nCreating a book for that author...")
    resp = client.post("/books/", json={
        "title": "1984",
        "genre": "Dystopian",
        "price": 12.99,
        "published_year": 1949,
        "author_id": author_id,
    })
    check(resp.status_code == 201, "book creation returns 201")
    book = resp.json()
    book_id = book["id"]

    print("\nCreating a book with a bad author_id (should fail cleanly)...")
    resp = client.post("/books/", json={
        "title": "Fake Book", "price": 5.0, "author_id": 9999
    })
    check(resp.status_code == 400, "book creation with invalid author_id returns 400")

    print("\nFetching the book back...")
    resp = client.get(f"/books/{book_id}")
    check(resp.status_code == 200, "get book returns 200")
    check(resp.json()["title"] == "1984", "returned book has the right title")
    check(resp.json()["author"]["name"] == "George Orwell", "nested author data comes back correctly")

    print("\nFetching the author with their books nested in...")
    resp = client.get(f"/authors/{author_id}")
    check(resp.status_code == 200, "get author returns 200")
    check(len(resp.json()["books"]) == 1, "author shows exactly one book")

    print("\nUpdating the book's price...")
    resp = client.put(f"/books/{book_id}", json={"price": 9.99})
    check(resp.status_code == 200, "book update returns 200")
    check(resp.json()["price"] == 9.99, "price actually changed")
    check(resp.json()["title"] == "1984", "title stayed the same (partial update)")

    print("\nFiltering books by genre...")
    resp = client.get("/books/", params={"genre": "dystop"})
    check(resp.status_code == 200 and len(resp.json()) == 1, "genre filter (partial, case-insensitive) finds the book")

    print("\nSearching books by title...")
    resp = client.get("/books/", params={"search": "984"})
    check(len(resp.json()) == 1, "title search finds the book")

    print("\nDeleting the book...")
    resp = client.delete(f"/books/{book_id}")
    check(resp.status_code == 204, "book delete returns 204")

    resp = client.get(f"/books/{book_id}")
    check(resp.status_code == 404, "deleted book returns 404 afterwards")

    print("\nDeleting a non-existent author...")
    resp = client.delete("/authors/99999")
    check(resp.status_code == 404, "deleting a missing author returns 404")

    print("\nCleaning up test author...")
    client.delete(f"/authors/{author_id}")

    print("\nAll checks passed.")


if __name__ == "__main__":
    run()
    # clean up the throwaway test db file
    if os.path.exists("test_library.db"):
        os.remove("test_library.db")
