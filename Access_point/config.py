# my_app/config.py
import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")
    # Example if you use a local DB or Postgres, etc.
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///mydatabase.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
