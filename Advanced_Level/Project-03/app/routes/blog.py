from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, jsonify
from flask_login import login_required, current_user
from slugify import slugify
from app import db
from app.models import Post, Comment, Like, Category, Tag
from app.forms import PostForm, CommentForm

blog_bp = Blueprint("blog", __name__)


@blog_bp.route("/")
def index():
    page = request.args.get("page", 1, type=int)
    category_id = request.args.get("category", None, type=int)
    tag_name = request.args.get("tag", None)
    search = request.args.get("search", "")

    query = Post.query.filter_by(is_published=True)

    if category_id:
        query = query.filter_by(category_id=category_id)

    if tag_name:
        query = query.join(Post.tags).filter(Tag.name == tag_name)

    if search:
        query = query.filter(
            (Post.title.ilike(f"%{search}%")) | (Post.content.ilike(f"%{search}%"))
        )

    posts = query.order_by(Post.created_at.desc()).paginate(page=page, per_page=6)
    categories = Category.query.all()
    popular_posts = Post.query.filter_by(is_published=True).order_by(Post.views.desc()).limit(5).all()

    return render_template(
        "blog/index.html",
        title="Blog",
        posts=posts,
        categories=categories,
        popular_posts=popular_posts,
        search=search,
    )


@blog_bp.route("/post/<string:slug>", methods=["GET", "POST"])
def post_detail(slug):
    post = Post.query.filter_by(slug=slug, is_published=True).first_or_404()
    post.views += 1
    db.session.commit()

    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You must be logged in to comment.", "warning")
            return redirect(url_for("auth.login"))

        comment = Comment(
            content=comment_form.content.data,
            user_id=current_user.id,
            post_id=post.id,
        )
        db.session.add(comment)
        db.session.commit()
        flash("Comment added!", "success")
        return redirect(url_for("blog.post_detail", slug=slug))

    user_liked = False
    if current_user.is_authenticated:
        user_liked = Like.query.filter_by(user_id=current_user.id, post_id=post.id).first() is not None

    related_posts = Post.query.filter(
        Post.category_id == post.category_id,
        Post.id != post.id,
        Post.is_published == True,
    ).limit(3).all()

    return render_template(
        "blog/post_detail.html",
        post=post,
        comment_form=comment_form,
        user_liked=user_liked,
        related_posts=related_posts,
        title=post.title,
    )


@blog_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_post():
    form = PostForm()
    form.category_id.choices = [(0, "-- Select Category --")] + [
        (c.id, c.name) for c in Category.query.all()
    ]

    if form.validate_on_submit():
        slug = slugify(form.title.data)
        existing = Post.query.filter_by(slug=slug).first()
        if existing:
            slug = f"{slug}-{Post.query.count() + 1}"

        post = Post(
            title=form.title.data,
            slug=slug,
            content=form.content.data,
            summary=form.summary.data,
            is_published=form.is_published.data,
            user_id=current_user.id,
            category_id=form.category_id.data if form.category_id.data != 0 else None,
        )

        tag_names = [t.strip() for t in form.tags.data.split(",") if t.strip()]
        for tag_name in tag_names:
            tag = Tag.query.filter_by(name=tag_name.lower()).first()
            if not tag:
                tag = Tag(name=tag_name.lower())
                db.session.add(tag)
            post.tags.append(tag)

        db.session.add(post)
        db.session.commit()
        flash("Post created successfully!", "success")
        return redirect(url_for("blog.post_detail", slug=post.slug))

    return render_template("blog/create_post.html", form=form, title="Create Post")


@blog_bp.route("/edit/<int:post_id>", methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user and not current_user.is_admin:
        abort(403)

    form = PostForm(obj=post)
    form.category_id.choices = [(0, "-- Select Category --")] + [
        (c.id, c.name) for c in Category.query.all()
    ]

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.summary = form.summary.data
        post.is_published = form.is_published.data
        post.category_id = form.category_id.data if form.category_id.data != 0 else None

        post.tags.clear()
        tag_names = [t.strip() for t in form.tags.data.split(",") if t.strip()]
        for tag_name in tag_names:
            tag = Tag.query.filter_by(name=tag_name.lower()).first()
            if not tag:
                tag = Tag(name=tag_name.lower())
                db.session.add(tag)
            post.tags.append(tag)

        db.session.commit()
        flash("Post updated successfully!", "success")
        return redirect(url_for("blog.post_detail", slug=post.slug))

    if request.method == "GET":
        form.tags.data = ", ".join([t.name for t in post.tags])

    return render_template("blog/edit_post.html", form=form, post=post, title="Edit Post")


@blog_bp.route("/delete/<int:post_id>", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user and not current_user.is_admin:
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash("Post deleted.", "info")
    return redirect(url_for("auth.dashboard"))


@blog_bp.route("/like/<int:post_id>", methods=["POST"])
@login_required
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    existing_like = Like.query.filter_by(user_id=current_user.id, post_id=post_id).first()

    if existing_like:
        db.session.delete(existing_like)
        db.session.commit()
        liked = False
    else:
        like = Like(user_id=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()
        liked = True

    return jsonify({"liked": liked, "count": post.like_count()})


@blog_bp.route("/comment/delete/<int:comment_id>", methods=["POST"])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.commenter != current_user and not current_user.is_admin:
        abort(403)
    post_slug = comment.post.slug
    db.session.delete(comment)
    db.session.commit()
    flash("Comment deleted.", "info")
    return redirect(url_for("blog.post_detail", slug=post_slug))
