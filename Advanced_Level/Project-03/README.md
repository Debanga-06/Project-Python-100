# 📝 Project 04 — Blog Website

> **Python Project #100** | Advanced Level | Flask · SQLAlchemy · Authentication

A fully-featured, production-ready blog platform built with Flask. Supports user authentication, post creation with categories & tags, a like/comment system, and a personal dashboard.

---

## 🚀 Features

| Feature | Details |
|---|---|
| 🔐 Authentication | Register, Login, Logout with hashed passwords (Bcrypt) |
| 📝 Post Management | Create, Edit, Delete posts with rich content |
| 📂 Categories & Tags | Organize posts with multi-tag support |
| ❤️ Like System | AJAX-powered like/unlike per user |
| 💬 Comments | Add & delete comments on posts |
| 📊 Dashboard | Stats: total posts, likes, views, comments |
| 🔍 Search & Filter | Search by keyword, filter by category/tag |
| 📄 Draft / Publish | Save as draft or publish immediately |
| 👁️ View Counter | Auto-increments on each post visit |
| 🛡️ CSRF Protection | Flask-WTF on all forms |
| 📱 Responsive | Bootstrap 5 mobile-friendly UI |

---

## 🗂️ Project Structure

```
project-04-blog-website/
├── app/
│   ├── __init__.py          # App factory (create_app)
│   ├── models.py            # User, Post, Comment, Like, Tag, Category
│   ├── forms.py             # WTForms: Register, Login, Post, Comment
│   ├── routes/
│   │   ├── auth.py          # /auth/register, login, logout, profile
│   │   ├── blog.py          # /blog/ CRUD, like, comment
│   │   └── main.py          # / home, /about
│   ├── templates/
│   │   ├── base.html
│   │   ├── auth/            # login, register, dashboard, profile
│   │   ├── blog/            # index, post_detail, create, edit
│   │   └── main/            # index, about
│   └── static/
│       ├── css/style.css
│       └── js/main.js
├── config.py                # Dev / Prod / Test configs
├── run.py                   # Entry point + CLI commands
├── requirements.txt
└── .env.example
```

---

## ⚙️ Setup & Installation

### 1. Clone & Navigate
```bash
git clone https://github.com/yourname/python-project-100.git
cd python-project-100/project-04-blog-website
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
cp .env.example .env
# Edit .env and set your SECRET_KEY
```

### 5. Initialize Database
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 6. Seed Sample Data (Optional)
```bash
flask seed-db
# Creates: admin user (admin@blog.com / admin123) + categories
```

### 7. Run the App
```bash
python run.py
# or
flask run
```

Open → **http://127.0.0.1:5000**

---

## 🗄️ Database Models

```
User ──┬──< Post >──< post_tags >──< Tag
       │     │
       │     ├──< Comment
       │     └──< Like
       │
       ├──< Comment
       └──< Like

Post >── Category
```

| Model | Key Fields |
|---|---|
| `User` | username, email, password_hash, is_admin |
| `Post` | title, slug, content, is_published, views |
| `Category` | name, description |
| `Tag` | name (many-to-many with Post) |
| `Comment` | content, user_id, post_id |
| `Like` | user_id, post_id (unique constraint) |

---

## 🔌 API Endpoints

| Method | Route | Description |
|---|---|---|
| GET | `/` | Home page |
| GET | `/blog/` | All posts (search, filter) |
| GET | `/blog/post/<slug>` | Post detail |
| GET/POST | `/blog/create` | Create post (auth required) |
| GET/POST | `/blog/edit/<id>` | Edit post (owner/admin) |
| POST | `/blog/delete/<id>` | Delete post |
| POST | `/blog/like/<id>` | Toggle like (JSON response) |
| POST | `/blog/comment/delete/<id>` | Delete comment |
| GET/POST | `/auth/register` | Register |
| GET/POST | `/auth/login` | Login |
| GET | `/auth/logout` | Logout |
| GET | `/auth/dashboard` | User dashboard |
| GET/POST | `/auth/profile` | Edit profile |

---

## 🔧 Flask CLI Commands

```bash
flask seed-db          # Seed categories + admin user
flask db migrate       # Generate migration
flask db upgrade       # Apply migration
flask shell            # Python shell with app context
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| **Flask 3.x** | Web framework |
| **SQLAlchemy** | ORM / Database |
| **Flask-Login** | Session-based authentication |
| **Flask-Bcrypt** | Password hashing |
| **Flask-Migrate** | Alembic DB migrations |
| **Flask-WTF** | Forms + CSRF protection |
| **python-slugify** | URL-friendly post slugs |
| **Bootstrap 5** | Responsive frontend |
| **SQLite** | Default DB (swap to PostgreSQL in prod) |

---

## 🌐 Production Deployment

```bash
# Switch to PostgreSQL
DATABASE_URL=postgresql://user:pass@host/dbname

# Use Gunicorn
pip install gunicorn
gunicorn -w 4 "run:app"
```

---

## 📸 Pages Overview

- **/** → Hero, featured posts, recent posts, categories
- **/blog/** → Paginated post list with search/filter sidebar
- **/blog/post/<slug>** → Full post, likes, comments, related posts
- **/auth/dashboard** → Stats card + post management table
- **/auth/profile** → Edit username, email, bio

---

## 🧠 Concepts Practiced

- Flask Application Factory pattern
- SQLAlchemy relationships (One-to-Many, Many-to-Many)
- Blueprint-based route organization
- Flask-Login session management
- CSRF-protected forms with Flask-WTF
- Database migrations with Alembic/Flask-Migrate
- Jinja2 templating with template inheritance
- AJAX fetch API for like toggle
- Slugified URLs for SEO-friendly posts

---

*Part of the **Python Project #100** series — Advanced Level Projects*