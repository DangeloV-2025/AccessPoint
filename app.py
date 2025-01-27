from flask import (Flask, render_template,
                   request, redirect,
                   session, url_for,
                   flash, send_from_directory,
                   abort
)
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from supabase import create_client, Client

import csv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


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

# Function to load scholarships from CSV
def load_scholarships():
    scholarships = []
    with open('Access_point/assets/csv/scholarships.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            scholarships.append(row)
    return scholarships


# # Scholarship model
# class Scholarship(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(200), nullable=False)
#     amount = db.Column(db.String(100), nullable=False)
#     deadline = db.Column(db.String(50), nullable=False)
#     description = db.Column(db.Text, nullable=False)
#     apply_link = db.Column(db.String(500), nullable=False)

#TODO: Make this method open for all of them
# Populate the database from a CSV file

def populate_from_csv():
    try:
        with open('Access_point/assets/csv/scholarships.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            scholarships = [
                {
                    'name': row['name'],
                    'amount': row['amount'],
                    'deadline': row['deadline'],
                    'description': row['description'],
                    'apply_link': row['apply_link']
                }
                for row in reader
            ]
            return scholarships
    except FileNotFoundError:
        print("Error: The file 'scholarships.csv' was not found.")
    except csv.Error as e:
        print(f"Error processing CSV file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


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

## SUPABASE LOGIN ATTEMPTS

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        try:
            # Supabase user sign-up
            response = supabase.auth.sign_up({"email": email, "password": password})
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("login"))
        except Exception as e:
            flash(f"Error during registration: {e}", "danger")
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        try:
            # Attempt to log in
            response = supabase.auth.sign_in_with_password({"email": email, "password": password})

            # If successful, redirect to dashboard
            if response.get("user"):
                session["user"] = response["user"]
                flash("Login successful!", "success")
                return redirect(url_for("dashboard"))
        except Exception as e:
            # Handle specific error messages
            error_message = str(e)
            if "Invalid login credentials" in error_message:
                flash("Incorrect email or password. Please try again.", "danger")
            else:
                flash("An unexpected error occurred. Please try again later.", "danger")
            print(f"Error during login: {e}")  # Debugging: Print the error

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logged out successfully.", "success")
    return redirect(url_for("login"))



@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        flash("Please log in to access the dashboard.", "warning")
        return redirect(url_for("login"))
    return render_template("dashboard.html", user=session["user"])




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

@app.route("/resources/scholarships")
def scholarships():
    scholarships = populate_from_csv()  # Load data from CSV
    return render_template("resources/scholarships.html", scholarships=scholarships)

@app.route("/resources/pre_college")
def Pre_college():
    scholarships = load_scholarships()  # Load data from CSV
    return render_template("resources/pre_colelege.html", scholarships=scholarships)


@app.route("/resources/<page>")
def resources(page):
    if page == "scholarships":
        abort(404)  # Prevent conflict
    try:
        return render_template(f"resources/{page}.html")
    except:
        abort(404)




if __name__ == '__main__':
    app.run(debug=True)
