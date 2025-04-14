import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

def init_db(app):
    # Use PostgreSQL database
    db_url = "postgresql://scrape_twitter_user:q34MX3VwkkpTs9jRquBoedjPRYxdaTqJ@dpg-cvufco9r0fns73823hcg-a.oregon-postgres.render.com/scrape_twitter"
    
    # Fix Postgres URL for SQLAlchemy 1.4+
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    # Initialize the app with the database extension
    db.init_app(app)
    
    return app 