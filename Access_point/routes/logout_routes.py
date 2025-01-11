from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from Access_point.supabase_client import supabase

auth_bp = Blueprint("logout", __name__)

@auth_bp.route("/logout")
def logout():
    """Log out the current user."""
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for("auth.login"))
