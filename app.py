from flask import Flask
from config import Config
from models import db, User
from flask_login import LoginManager

# Create Flask app instance
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# Import routes after app is created to avoid circular imports
from routes import *

# Function to create a default admin user
def create_admin():
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='admin').first():
            admin_user = User(username='admin', role='admin')
            admin_user.set_password('adminpass') # Change this in production
            db.session.add(admin_user)
            db.session.commit()
            print("Admin user created.")

if __name__ == '__main__':
    create_admin() # Create admin on first run
    app.run(debug=True)