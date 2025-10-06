#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Run database migrations and create the admin user
python -c "
import os
from app import app, db
from models import User

print('Connecting to the database...')
app.app_context().push()

print('Creating all database tables...')
db.create_all()

admin_username = 'admin'
admin_password = 'adminpass'

if not User.query.filter_by(username=admin_username).first():
    print(f'Admin user \"{admin_username}\" not found, creating one...')
    admin_user = User(username=admin_username, role='admin')
    admin_user.set_password(admin_password)
    db.session.add(admin_user)
    db.session.commit()
    print('Admin user created successfully!')
else:
    print(f'Admin user \"{admin_username}\" already exists.')
"
