# run.py
from Access_point import create_app
import csv
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
