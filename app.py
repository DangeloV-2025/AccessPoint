from flask import Flask, render_template, send_from_directory, abort
from flask_sqlalchemy import SQLAlchemy
import csv
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scholarships.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Path to the blog_posts directory
BLOG_POSTS_DIR = "blog_posts"


def load_blog_post(slug):
    """Loads a blog post by its slug."""
    post_dir = os.path.join(BLOG_POSTS_DIR, slug)
    if not os.path.isdir(post_dir):
        return None  # Return None if the directory doesn't exist

    # Read metadata
    metadata_file = os.path.join(post_dir, "metadata.txt")
    if not os.path.exists(metadata_file):
        return None  # Return None if metadata.txt doesn't exist

    metadata = {}
    with open(metadata_file, "r", encoding="utf-8") as f:
        for line in f:
            key, value = line.strip().split(": ", 1)
            metadata[key] = value

    # Read content
    content_file = os.path.join(post_dir, "content.txt")
    if not os.path.exists(content_file):
        return None  # Return None if content.txt doesn't exist

    with open(content_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Combine metadata and content
    metadata["content"] = content
    return metadata


# Scholarship model
class Scholarship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.String(100), nullable=False)
    deadline = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    apply_link = db.Column(db.String(500), nullable=False)

# Populate the database from a CSV file
def populate_from_csv():
    if Scholarship.query.count() == 0:  # Avoid duplicates
        with open('scholarships.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            scholarships = [
                Scholarship(
                    name=row['name'],
                    amount=row['amount'],
                    deadline=row['deadline'],
                    description=row['description'],
                    apply_link=row['apply_link']
                ) for row in reader
            ]
            db.session.add_all(scholarships)
            db.session.commit()

# Initialize the database
with app.app_context():
    try:
        db.create_all()
        populate_from_csv()
    except:
        print("We haven't reached that yet")

@app.route("/")
def home():
    """Home page showing a list of blog posts."""
    posts = []
    for slug in os.listdir(BLOG_POSTS_DIR):
        post = load_blog_post(slug)
        if post:
            posts.append(post)
    return render_template("index.html", posts=posts)


@app.route("/blog/<slug>")
def blog_post(slug):
    """Route to display an individual blog post."""
    post = load_blog_post(slug)
    if not post:
        abort(404)  # Return a 404 error if the post is not found
    return render_template("blog_post.html", post=post)


# Serve the 'assets' folder
@app.route('/assets/<path:filename>')
def assets(filename):
    return send_from_directory('assets', filename)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/scholarships")
def scholarships():
    return render_template("scholarships.html")


#TODO: Fix scholarships population and then repeat process for the other 2
# @app.route('/resources/scholarships')
# def scholarships():
#     scholarships = Scholarship.query.all()
#     return render_template('resources/scholarships.html', scholarships=scholarships)

if __name__ == '__main__':
    app.run(debug=True)
