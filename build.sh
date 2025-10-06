#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Create database tables using the Flask app context
echo "from app import app, db; app.app_context().push(); db.create_all()" | python

# Create the initial admin user (if it doesn't exist)
echo "from app import app, db; from models import User; app.app_context().push(); \
if not User.query.filter_by(username='admin').first(): \
    admin_user = User(username='admin', role='admin'); \
    admin_user.set_password('adminpass'); \
    db.session.add(admin_user); \
    db.session.commit(); \
    print('Admin user created successfully!') \
else: \
    print('Admin user already exists.')" | python
