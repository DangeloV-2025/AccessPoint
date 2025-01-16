# my_app/routes/resource_routes.py
from flask import Blueprint, render_template, abort
import csv
from Access_point.supabase_client import supabase


resource_bp = Blueprint("resource", __name__)


@resource_bp.route("/resources/scholarships")
def scholarships():
    """Fetch and display scholarships from Supabase."""
    try:
        # Fetch data from Supabase
        response = supabase.table("scholarships").select("*").execute()
        scholarships = response.data  # This contains the fetched rows

        # Debugging: Print the response
        print(f"Response Data: {scholarships}")

        # Default to an empty list if no data
        if scholarships is None:
            scholarships = []
    except Exception as e:
        print(f"Error fetching scholarships: {e}")
        scholarships = []
    try:
        return render_template("resources/scholarships.html", scholarships=scholarships)
    except:
        print("Error accessing HTML")
        abort(404)

    
@resource_bp.route("/resources/fly_ins")
def fly_ins():
    print("Route was hit!")  # Debugging
    """Fetch and display fly-ins from Supabase."""
    try:
        # Fetch data from Supabase
        response = supabase.table("fly_ins").select("*").execute()
        fly_ins = response.data  # Contains the fetched rows

        # Debugging: Print the fetched data for inspection
        print(f"Fetched fly_ins data: {fly_ins}")

        # Default to an empty list if no data is found
        if not fly_ins:
            fly_ins = []
    except Exception as e:
        print(f"Error fetching fly_ins: {e}")
        fly_ins = []

    # Render the template with the fetched fly_ins data
    try:
        return render_template("resources/fly_ins.html", fly_ins=fly_ins)
    except Exception as e:
        print(f"Error rendering template: {e}")
        abort(404)

# @resource_bp.route("/resources/fly-ins")
# def fly_ins():
#     print("Route was hit!")  # Debugging
#     return "Debugging Route: Fly-Ins"

def load_scholarships():
    scholarships = []
    with open('resource_content/Scholarships_PlaceHolder - Sheet2.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            scholarships.append(row)
    return scholarships



@resource_bp.route("/resources/pre-college-programs")
def pre_college():
    data = load_scholarships()  # Example usage, or different loader function
    return render_template("resources/precolelege.html", scholarships=data)

@resource_bp.route("/resources/<page>")
def resources(page):
    if page == "scholarships":
        abort(404)  # Prevent conflict
    try:
        return render_template(f"resources/{page}.html")
    except:
        abort(404)
