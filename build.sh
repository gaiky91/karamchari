#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# This command is a placeholder to create the DB tables.
# It uses app.app_context() to run db.create_all()
# We need a small Python script to do this.
echo "from app import app, db; app.app_context().push(); db.create_all()" | python