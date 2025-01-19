from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from Access_point.supabase_client import supabase
from Access_point.routes.utils import login_required

dashboard_bp = Blueprint("dashboard", __name__)  # Unique name for dashboard blueprint

@login_required

@dashboard_bp.route("/dashboard")
def dashboard():
    """User dashboard."""
    if "user_id" not in session:
        flash("Please log in to access the dashboard.", "warning")
        return redirect(url_for("auth.login"))

    # Fetch user-specific data (if any) from the database
    user_id = session["user_id"]
    response = supabase.table("users").select("*").eq("id", user_id).execute()
    user = response.data[0] if response.data else {}

    return render_template("auth/dashboard.html", user=user)


