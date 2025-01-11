from flask import session, redirect, url_for, flash

def login_required(func):
    """Decorator to require login."""
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("You need to log in to access this page.", "danger")
            return redirect(url_for("auth.login"))
        return func(*args, **kwargs)
    return wrapper
