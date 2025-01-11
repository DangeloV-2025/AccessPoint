# my_app/models.py
from . import db

class Scholarship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.String(100), nullable=False)
    deadline = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    apply_link = db.Column(db.String(500), nullable=False)
