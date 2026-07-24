# Library RESTful API

A CRUD API built with FastAPI and SQLAlchemy for managing a small library of authors and books. Built for my Python 100 advanced project to cover the basics of building a real REST API backed by an actual database, not just an in-memory list.

## What this project actually does

In plain terms: this is a little program that keeps track of books and the authors who wrote them, and lets other programs (or a person, through a browser or a tool like Postman) ask it to add, look up, change, or remove that information over the internet.

Think of it like the backend of a library management system. Instead of a database admin typing SQL commands directly into a database, this gives you a proper "front door" - a set of web addresses (endpoints) that a website, a mobile app, or anyone with the right tool can call to say things like "add this new book," "show me every book by this author," "this book's price changed, update it," or "remove this book, it's out of print."

Everything gets saved permanently in a small database file, so if you stop the program and start it again, nothing is lost - all the authors and books you added are still there.

A few concrete things you can actually do with it:
- Add a new author (say, "George Orwell")
- Add a book and attach it to that author (say, "1984," published 1949)
- Look up every book by a specific author
- Search for a book by (part of) its title
- Filter books by genre
- Change a book's price or details without having to re-enter everything
- Delete a book, or delete an author entirely (which removes their books too)

It doesn't have a visual interface (no buttons or web pages to click through) - it's a backend service, meant to be talked to by other software. That said, FastAPI gives it a free built-in test page (at `/docs`) where a person can try out every one of these actions from a browser without writing any code, just to see it working.

## Why FastAPI over Flask

Went with FastAPI instead of Flask for this one. Flask is great and totally valid for this kind of project too, but FastAPI gives you request validation (via Pydantic) and interactive API docs completely for free, which saves a lot of boilerplate you'd otherwise write by hand in Flask (marshmallow schemas, flask-restx, etc). If your course specifically wants Flask, the same structure (routes / models / schemas / crud separated into files) translates over pretty directly, just swap the router/dependency-injection parts for Flask blueprints and request.get_json().

## What's in here

Two related resources:
- **Authors** - name, country
- **Books** - title, genre, price, published year, and a foreign key back to an author

Every resource supports full CRUD: Create, Read, Update, Delete. Books can also be filtered by genre, filtered by author, or searched by title.

## Project layout

```
restful_api/
├── app/
│   ├── main.py          -> creates the FastAPI app, wires up routers
│   ├── database.py      -> SQLAlchemy engine/session setup
│   ├── models.py        -> the actual database tables (Author, Book)
│   ├── schemas.py        -> Pydantic models used for validation/responses
│   ├── crud.py           -> the functions that actually talk to the DB
│   └── routers/
│       ├── authors.py    -> /authors endpoints
│       └── books.py      -> /books endpoints
├── test_api.py           -> quick script that exercises every endpoint
├── requirements.txt
└── .gitignore
```

Kept the database logic (`crud.py`) separate from the route handlers (`routers/`) on purpose. The routes only deal with HTTP concerns - status codes, request/response shapes - and crud.py only deals with the database. Makes both pieces a lot easier to reason about and test on their own.

## Running it

Install dependencies:
```
pip install -r requirements.txt
```

Start the server:
```
uvicorn app.main:app --reload
```

That's it - SQLite creates `library.db` automatically the first time you run it, no separate database setup needed. Open `http://127.0.0.1:8000/docs` in a browser and you get a full interactive UI (Swagger) where you can try every endpoint without writing a single curl command.

## Endpoints

**Authors**
| Method | Path | What it does |
|---|---|---|
| POST | /authors/ | create an author |
| GET | /authors/ | list authors (paginated) |
| GET | /authors/{id} | get one author, with their books nested in |
| PUT | /authors/{id} | update an author (partial updates work) |
| DELETE | /authors/{id} | delete an author (and their books, cascade) |

**Books**
| Method | Path | What it does |
|---|---|---|
| POST | /books/ | create a book (needs a valid author_id) |
| GET | /books/ | list books, with optional ?genre=, ?author_id=, ?search= filters |
| GET | /books/{id} | get one book, with its author nested in |
| PUT | /books/{id} | update a book (partial updates work) |
| DELETE | /books/{id} | delete a book |

## Quick example

Create an author:
```
curl -X POST http://127.0.0.1:8000/authors/ \
  -H "Content-Type: application/json" \
  -d '{"name": "George Orwell", "country": "United Kingdom"}'
```

Add a book for that author (assuming the author came back with id 1):
```
curl -X POST http://127.0.0.1:8000/books/ \
  -H "Content-Type: application/json" \
  -d '{"title": "1984", "genre": "Dystopian", "price": 12.99, "published_year": 1949, "author_id": 1}'
```

Search for it:
```
curl "http://127.0.0.1:8000/books/?search=1984"
```

## A few things worth pointing out

- **Partial updates actually work.** PUT on a book only overwrites the fields you send, not everything - this is handled with `exclude_unset=True` on the Pydantic side rather than requiring the full object every time.
- **Foreign key validation.** Trying to create a book with an author_id that doesn't exist gets you a clean 400 error instead of a database crash.
- **Cascade delete.** Deleting an author deletes their books along with them, instead of leaving orphaned rows in the books table.
- **CORS is wide open** (`allow_origins=["*"]`) since this is a learning project meant to be hit from anywhere during testing. Lock this down to specific origins before using this pattern in anything real.

## Testing it

`test_api.py` runs through the whole CRUD cycle against a throwaway test database (doesn't touch your real library.db) and checks status codes and response data at each step:
```
python test_api.py
```

## Things I'd add with more time

- JWT-based auth so not just anyone can create/delete records
- Switch from SQLite to Postgres and use Alembic for actual migrations instead of `create_all`
- Rate limiting
- Proper pytest test suite with fixtures instead of one script that runs top to bottom
