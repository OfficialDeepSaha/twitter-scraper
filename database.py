import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

def init_db(app):
    # Configure the database
    db_url = os.environ.get("DATABASE_URL")
    if db_url is None:
        db_url = "sqlite:///twitter_scraper.db"  # Fallback to SQLite if no DB URL is provided
        
    # Fix Postgres URL for SQLAlchemy 1.4+
    if db_url and db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    # Initialize the app with the database extension
    db.init_app(app)
    
    return app 