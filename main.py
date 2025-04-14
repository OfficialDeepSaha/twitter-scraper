from app import app, db
import models  # Import to ensure models are registered with SQLAlchemy

with app.app_context():
    # Create all tables in the database
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
