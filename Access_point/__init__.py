# my_app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

db = SQLAlchemy()  # We define db here, bfut we only init_app inside create_app

def create_app():
    """Application factory: creates and configures the Flask app."""
    # Load environment variables
    load_dotenv()

    app = Flask(__name__, instance_relative_config=False)
    # Load configurations from config.py
    app.config.from_object('Access_point.config.Config')

    # Initialize Flask extensions
    db.init_app(app) 

    # Register Blueprints
    from Access_point.routes.main_routes import main_bp
    from Access_point.routes.auth_routes import auth_bp
    from Access_point.routes.resource_routes import resource_bp
    from Access_point.routes.dashboard_route import dashboard_bp

    #print("Registering Blueprint: main_bp")
    app.register_blueprint(main_bp)

    #print("Registering Blueprint: auth_bp")
    app.register_blueprint(auth_bp)

    #print("Registering Blueprint: resource_bp")
    app.register_blueprint(resource_bp)

    #print("Registering Blueprint: dashboard_bp")
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")

    # If you want to do any "create_all" or DB seeding on first startup,
    # you can do it inside an app context:
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print(f"Database creation error: {e}")

    return app
