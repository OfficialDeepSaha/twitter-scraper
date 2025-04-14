import os
from app import app, db
import models  # Import to ensure models are registered with SQLAlchemy

with app.app_context():
    # Create all tables in the database
    db.create_all()

if __name__ == "__main__":
    # Get port from environment variable or default to 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
