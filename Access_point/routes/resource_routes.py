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
        # response = supabase.table("scholarships").select("*").execute()
        # scholarships = response.data  # This contains the fetched rows
        scholarships = populate_data('Access_point/assets/csv/scholarships.csv')
        print(scholarships)

        # Uncomment for debugging
        # print(f"Fetched scholarships data: {scholarships}")

        # Default to an empty list if no data
        if not scholarships:
            scholarships = []
        else:
            current_date = datetime.now()
            date_format = "%Y %B %d"  # Format: Year Month Day (e.g., "2024 August 12")

            for scholarship in scholarships:
                # Ensure 'deadline' exists and is not None
                if 'deadline' in scholarship and scholarship['deadline']:

                    deadline_date = datetime.strptime(scholarship['deadline'], date_format) # Converts to comparable time

                    # Check if the deadline has passed
                    if deadline_date < current_date:
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

from datetime import datetime
from flask import render_template, abort

@resource_bp.route("/resources/fly_ins")
def fly_ins():
    """Fetch and display fly-ins from Supabase or CSV file."""
    try:
        # Fetch data from CSV
        fly_ins = populate_data('Access_point/assets/csv/fly_ins.csv')

        # Default to an empty list if no data is found
        if not fly_ins:
            fly_ins = []
        else:
            # Get the current date in 'dd-Mon-yy' format (e.g., '27-Jan-25')
            current_date = datetime.now()
            date_format = "%Y %B %d"  # Format: Year Month Day (e.g., "2024 August 12")

            # Process each fly-in entry
            for fly_in in fly_ins:
                # Ensure 'deadline' exists and is not None
                if 'deadline' in fly_in and fly_in['deadline']:
                    deadline_date = datetime.strptime(fly_in['deadline'], date_format) # Converts to comparable time
                    # Check if the deadline has passed
                    if deadline_date < current_date:
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


@resource_bp.route("/resources/pre_college")
def pre_college():
    """Fetch and display pre_college from Supabase."""
    print("Route was hit!")  # Debugging

    try:
        # Fetch data from Supabase
        # response = supabase.table("pre_college").select("*").execute()
        # pre_college = response.data
        pre_college = populate_data('Access_point/assets/csv/precollege_programs.csv')

        # Default to an empty list if no data is found
        if not pre_college:
            pre_college = []
        else:
            # Get the current date in 'dd-Mon-yy' format (e.g., '27-Jan-25')
            current_date = datetime.now()
            date_format = "%Y %B %d"  # Format: Year Month Day (e.g., "2024 August 12")

            # Process each pre-college entry
            for entry in pre_college:
                # Ensure 'deadline' exists and is not None
                if 'deadline' in entry and entry['deadline']:
                    deadline_date = datetime.strptime(entry['deadline'], date_format)  # Converts to comparable time
                    # Check if the deadline has passed
                    if deadline_date < current_date:
                        entry['is_expired'] = True
                    else:
                        entry['is_expired'] = False
                else:
                    # Default for pre-colleges without a deadline
                    entry['is_expired'] = True

            # Sort pre-colleges: Open first, then expired
            pre_college.sort(key=lambda x: x['is_expired'])

    except Exception as e:
        print(f"Error fetching pre-college: {e}")
        pre_college = []

    # Render the template with the fetched pre_college data
    try:
        print(pre_college)
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




# def populate_from_csv(link):
#     try:
#         with open(link, newline='', encoding='utf-8') as csvfile:
#             reader = csv.DictReader(csvfile)
#             scholarships = [
#                 {
#                     'name': row['name'],
#                     'amount': row['amount'],
#                     'deadline': row['deadline'],
#                     'description': row['description'],
#                     'apply_link': row['apply_link']
#                 }
#                 for row in reader
#             ]
#             return scholarships
#     except FileNotFoundError:
#         print("Error: The file 'scholarships.csv' was not found.")
#     except csv.Error as e:
#         print(f"Error processing CSV file: {e}")
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")

# def populate_fly_ins(link):
#     try:
#         with open(link, newline='', encoding='utf-8') as csvfile:
#             reader = csv.DictReader(csvfile)



#             fly_in = [
#                 {
#                     'host_institution': row['host_institution'],
#                     'program': row['program'],
#                     'deadline': row['deadline'],
#                     'description': row['description'],
#                     'apply_link': row['apply_link']
#                 }
#                 for row in reader
#             ]
#             return fly_in
#     except FileNotFoundError:
#         print("Error: The file was not found.")
#     except csv.Error as e:
#         print(f"Error processing CSV file: {e}")
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")

def populate_data(link):
    """
    Generalized function to populate data from a CSV file.

    Args:
        link (str): Path to the CSV file.

    Returns:
        list: A list of dictionaries with data from the CSV file.
    """
    try:
        with open(link, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            # Automatically extract all fields from the header row
            data = [row for row in reader]
            return data
    except FileNotFoundError:
        print(f"Error: The file '{link}' was not found.")
    except csv.Error as e:
        print(f"Error processing CSV file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
