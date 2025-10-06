from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(256))
    role = db.Column(db.String(10), index=True) # 'admin', 'company', 'vendor'

    company = db.relationship('Company', backref='user', uselist=False)
    vendor = db.relationship('Vendor', backref='user', uselist=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), unique=True)
    address = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    employees = db.relationship('Employee', backref='company', lazy='dynamic')

    def __repr__(self):
        return f'<Company {self.name}>'

class Vendor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), unique=True)
    address = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    employees = db.relationship('Employee', backref='vendor', lazy='dynamic')

    # For reputation score calculation
    @property
    def reputation_score(self):
        total_employees = self.employees.count()
        if total_employees == 0:
            return "N/A" # No employees to judge by yet

        # Criteria 1: Longevity (average tenure in days)
        total_tenure = 0
        active_employees = 0
        for emp in self.employees.all():
            end_date = emp.leaving_date or date.today()
            tenure = (end_date - emp.joining_date).days
            total_tenure += tenure
            if not emp.leaving_date:
                active_employees += 1

        avg_tenure = total_tenure / total_employees

        # Criteria 2: Employee Retention Rate
        retention_rate = (active_employees / total_employees) * 100

        # Simple weighted score: 60% for tenure, 40% for retention
        # We normalize tenure by a factor (e.g., 365 days = max points for this part)
        score = (min(avg_tenure / 365, 1) * 60) + (retention_rate / 100 * 40)
        return f"{score:.2f} / 100"

    def __repr__(self):
        return f'<Vendor {self.name}>'

class Employee(db.Model):
    # Aadhar card is a 12-digit number, stored as a string.
    aadhar_card = db.Column(db.String(12), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    mobile_number = db.Column(db.String(15))
    permanent_address = db.Column(db.String(250))
    present_address = db.Column(db.String(250))
    previous_job = db.Column(db.String(100))
    duration = db.Column(db.String(50)) # e.g., "2 years"
    previous_salary = db.Column(db.String(50))
    type_of_job = db.Column(db.String(100)) # e.g., "Welder", "Electrician"
    joining_date = db.Column(db.Date, default=date.today)
    leaving_date = db.Column(db.Date, nullable=True)

    # Relationships
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'), nullable=True) # Nullable for direct hires

    def __repr__(self):
        return f'<Employee {self.name} ({self.aadhar_card})>'
