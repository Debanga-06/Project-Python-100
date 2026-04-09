from flask import Blueprint, render_template
from app.models import Post, Category, User

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    featured_posts = Post.query.filter_by(is_published=True).order_by(Post.views.desc()).limit(3).all()
    recent_posts = Post.query.filter_by(is_published=True).order_by(Post.created_at.desc()).limit(6).all()
    categories = Category.query.all()
    top_authors = User.query.join(User.posts).filter(Post.is_published == True).distinct().limit(4).all()
    return render_template(
        "main/index.html",
        title="Home",
        featured_posts=featured_posts,
        recent_posts=recent_posts,
        categories=categories,
        top_authors=top_authors,
    )


@main_bp.route("/about")
def about():
    return render_template("main/about.html", title="About")
