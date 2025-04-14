#!/bin/bash
# Exit on error
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Create database tables
python -c "from app import app, db; import models; app.app_context().push(); db.create_all()" 