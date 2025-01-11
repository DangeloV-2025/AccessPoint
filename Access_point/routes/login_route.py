from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from Access_point.supabase_client import supabase

auth_bp = Blueprint("login", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Log in an existing user."""
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        try:
            # Authenticate with Supabase
            response = supabase.auth.sign_in_with_password({"email": email, "password": password})

            # If successful, save user session
            if "user" in response:
                user = response["user"]
                session["user_id"] = user["id"]
                session["email"] = user["email"]

                flash("Login successful!", "success")
                return redirect(url_for("dashboard.dashboard"))
            else:
                flash("Invalid email or password.", "danger")
        except Exception as e:
            flash(f"An error occurred: {e}", "danger")

    return render_template("auth/login.html")
