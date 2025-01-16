from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from Access_point.supabase_client import supabase

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")  # Added URL prefix for clarity

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """Register a new user."""
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        try:
            auth_response = supabase.auth.sign_up({"email": email, "password": password})
            print(f"Registration response: {auth_response}")

            # Check for errors
            if hasattr(auth_response, "error") and auth_response.error:
                flash(auth_response.error.message, "danger")
            else:
                flash("Registration successful! Please log in.", "success")
                return redirect(url_for("auth.login"))
        except Exception as e:
            flash("Error during registration. Please try again.", "danger")
            print(f"Registration error: {e}")

    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Log in an existing user."""
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        try:
            # Authenticate with Supabase
            auth_response = supabase.auth.sign_in_with_password({"email": email, "password": password})
            print(f"Login response: {auth_response}")

            # Check for a valid user
            if auth_response.user:
                session["user"] = {
                    "id": auth_response.user.id,
                    "email": auth_response.user.email
                }
                flash("Login successful!", "success")
                print("login succesful")
                return redirect(url_for("auth.dashboard"))
            else:
                flash("Invalid email or password.", "danger")
        except Exception as e:
            flash("Error during login. Please try again.", "danger")
            print(f"Login error: {e}")

    return render_template("auth/login.html")


@auth_bp.route("/dashboard")
def dashboard():
    """Display the user dashboard."""
    if "user" not in session:
        flash("You need to log in first.", "warning")
        return redirect(url_for("auth.login"))

    return render_template("auth/dashboard.html", user=session["user"])


@auth_bp.route("/logout")
def logout():
    """Log out the current user."""
    session.pop("user", None)  # Clear session
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.logout"))

#       ________                     .__          
#  /  _____/  ____   ____   ____ |  |   ____  
# /   \  ___ /  _ \ /  _ \ / ___\|  | _/ __ \ 
# \    \_\  (  <_> |  <_> ) /_/  >  |_\  ___/ 
#  \______  /\____/ \____/\___  /|____/\___  >
#         \/             /_____/           \/ 


@auth_bp.route("/google-login")
def google_login():
    """Redirect user to Google sign-in via Supabase."""
    try:
        # Initiate Google OAuth
        auth_response = supabase.auth.sign_in_with_oauth(
            {
                "provider": "google",
                "options": {"redirect_to": "https://jzcjalkrgyjunvkzhonu.supabase.co/auth/v1/callback"},
            }
        )
        # Redirect user to the URL for Google sign-in
        return redirect(auth_response.url)  # Use the `url` attribute of the OAuthResponse object
    except Exception as e:
        flash("Error initiating Google sign-in. Please try again.", "danger")
        print(f"Google Login Error: {e}")
        return redirect(url_for("auth.login"))
    


@auth_bp.route("/google-callback")
def google_callback():
    """Handle the callback from Google after login."""
    try:
        # This assumes Supabase automatically manages sessions after OAuth
        session_data = supabase.auth.get_session()
        if session_data:
            session["user"] = {
                "id": session_data.user.id,
                "email": session_data.user.email,
                "provider": "google",
            }
            flash("Login successful via Google!", "success")
            return redirect(url_for("auth.dashboard"))
        else:
            flash("Failed to log in via Google. Please try again.", "danger")
    except Exception as e:
        flash("Error during Google login. Please try again.", "danger")
        print(f"Google Callback Error: {e}")

    return redirect(url_for("auth.login"))
