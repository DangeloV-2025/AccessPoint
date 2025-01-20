# my_app/routes/main_routes.py
import os
from flask import Blueprint, render_template, abort, send_from_directory
from Access_point.blog_utils import load_blog_post

main_bp = Blueprint("main", __name__)

BLOG_POSTS_DIR = "Access_point/blog_posts"

@main_bp.route("/")
def home():
    """Home page showing a list of blog posts."""
    posts = []
    print(f"Looking for blog posts in: {BLOG_POSTS_DIR}")
    for slug in os.listdir(BLOG_POSTS_DIR):
        post_path = os.path.join(BLOG_POSTS_DIR, slug)
        print(f"Checking path: {post_path}")
        if os.path.isdir(post_path):  # Only process directories
            post = load_blog_post(slug)
            if post:
                posts.append(post)
            else:
                print(f"Failed to load post for slug: {slug}")
    return render_template("index.html", posts=posts)


@main_bp.route("/blog/<slug>")
def blog_post(slug):
    """Route to display an individual blog post."""
    post = load_blog_post(slug)
    if not post:
        abort(404)
    return render_template("blog_post.html", post=post)


@main_bp.route('/assets/<path:filename>')
def assets(filename):
    return send_from_directory('assets', filename)

@main_bp.route("/about")
def about():
    return render_template("about.html")

@main_bp.route("/contact")
def contact():
    return render_template("contact.html")