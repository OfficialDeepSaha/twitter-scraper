#!/bin/bash
# Exit on error
set -o errexit

# Install Python dependencies with specific order for compatibility
pip install numpy==1.24.3
pip install psycopg2-binary==2.9.9
pip install -r requirements.txt

# Create database tables
python -c "from app import app, db; import models; app.app_context().push(); db.create_all()" 