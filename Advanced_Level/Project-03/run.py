from app import create_app, db
from app.models import User, Post, Category, Tag, Comment, Like

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "User": User,
        "Post": Post,
        "Category": Category,
        "Tag": Tag,
        "Comment": Comment,
        "Like": Like,
    }


@app.cli.command("seed-db")
def seed_db():
    """Seed the database with sample data."""
    # Create categories
    categories = ["Technology", "Travel", "Food", "Health", "Science"]
    for name in categories:
        if not Category.query.filter_by(name=name).first():
            db.session.add(Category(name=name, description=f"Posts about {name.lower()}"))

    # Create admin user
    if not User.query.filter_by(username="admin").first():
        admin = User(username="admin", email="admin@blog.com", is_admin=True)
        admin.set_password("admin123")
        db.session.add(admin)

    db.session.commit()
    print("✅ Database seeded successfully!")


if __name__ == "__main__":
    app.run(debug=True)
