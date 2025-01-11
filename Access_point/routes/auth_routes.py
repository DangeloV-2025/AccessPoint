from flask import Blueprint, render_template, request, redirect, url_for, flash
from Access_point.supabase_client import supabase

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """Register a new user."""
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        try:
            # Sign up the user in Supabase
            response = supabase.auth.sign_up({"email": email, "password": password})
            if response.get("error"):
                flash(f"Error: {response['error']['message']}", "danger")
                return redirect(url_for("auth.register"))

            # Store additional user information in the 'users' table
            user_data = {"id": response["user"]["id"], "email": email, "name": name}
            supabase.table("users").insert(user_data).execute()

            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("auth.login"))
        except Exception as e:
            flash(f"Error during registration: {e}", "danger")

    return render_template("auth/register.html")
