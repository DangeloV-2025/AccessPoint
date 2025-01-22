# my_app/routes/resource_routes.py
from flask import Blueprint, render_template, abort
import csv
from Access_point.supabase_client import supabase
from datetime import datetime 


resource_bp = Blueprint("resource", __name__)


@resource_bp.route("/resources/scholarships")
def scholarships():
    """Fetch and display scholarships from Supabase."""
    try:
        # Fetch data from Supabase
        response = supabase.table("scholarships").select("*").execute()
        scholarships = response.data  # This contains the fetched rows
        
        # Uncomment for debugging
        # print(f"Fetched scholarships data: {scholarships}") 

        # Default to an empty list if no data
        if not scholarships:
            scholarships = []
        else:
            current_date = datetime.now().strftime('%Y-%m-%d')
            for scholarship in scholarships:
                # Ensure 'deadline' exists and is not None
                if 'deadline' in scholarship and scholarship['deadline']:
                    # Check if the deadline has passed
                    if scholarship['deadline'] < current_date:
                        scholarship['is_expired'] = True
                    else:
                        scholarship['is_expired'] = False
                else:
                    # Default for scholarships without a deadline
                    scholarship['is_expired'] = True
            scholarships.sort(key=lambda x: x['is_expired'])
    except Exception as e:
        print(f"Error fetching scholarships: {e}")
        scholarships = []

    # Render the template with the fetched scholarships data
    try:
        return render_template("resources/scholarships.html", scholarships=scholarships)
    except:
        print("Error accessing HTML")
        abort(404)

    
@resource_bp.route("/resources/fly_ins")
def fly_ins():
    """Fetch and display fly-ins from Supabase."""
    print("Route was hit!")  # Debugging

    try:
        # Fetch data from Supabase
        response = supabase.table("fly_ins").select("*").execute()
        fly_ins = response.data

        # Uncomment for debugging
        # print(f"Fetched fly_ins data: {fly_ins}") 

        # Default to an empty list if no data is found
        if not fly_ins:
            fly_ins = []
        else:
            # Get the current date
            current_date = datetime.now().strftime('%Y-%m-%d')

            # Process fly-ins to determine expiration
            for fly_in in fly_ins:
                # Ensure 'deadline' exists and is not None
                if 'deadline' in fly_in and fly_in['deadline']:
                    # Check if the deadline has passed
                    if fly_in['deadline'] < current_date:
                        fly_in['is_expired'] = True
                    else:
                        fly_in['is_expired'] = False
                else:
                    # Default for fly-ins without a deadline
                    fly_in['is_expired'] = True

            # Sort fly-ins: Open first, then expired
            fly_ins.sort(key=lambda x: x['is_expired'])
    except Exception as e:
        print(f"Error fetching fly_ins: {e}")
        fly_ins = []

    # Render the template with the fetched fly-ins data
    try:
        return render_template("resources/fly_ins.html", fly_ins=fly_ins)
    except Exception as e:
        print(f"Error rendering template: {e}")
        abort(404)


def load_scholarships():
    scholarships = []
    with open('resource_content/Scholarships_PlaceHolder - Sheet2.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            scholarships.append(row)
    return scholarships



@resource_bp.route("/resources/pre_college")
def pre_college():
    """Fetch and display pre_college from Supabase."""
    print("Route was hit!")  # Debugging
    
    try:
        # Fetch data from Supabase
        response = supabase.table("pre_college").select("*").execute()
        pre_college = response.data
        print(pre_college)

        # Debugging: Log the fetched data
        print(f"Fetched pre college data: {pre_college}")

        # Default to an empty list if no data is found
        if not pre_college:
            pre_college = []
    except Exception as e:
        print(f"Error fetching pre-college: {e}")
        pre_college = []

    # Render the template with the fetched pre_college data
    try:
        return render_template("resources/pre_college.html", pre_college=pre_college)
    except Exception as e:
        print(f"Error rendering template: {e}")
        abort(404)



@resource_bp.route("/resources/<page>")
def resources(page):
    if page == "scholarships":
        abort(404)  # Prevent conflict
    try:
        return render_template(f"resources/{page}.html")
    except:
        abort(404)
