from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from wtforms_sqlalchemy.fields import QuerySelectField
from models import Vendor, Company, Employee

def company_query():
    return Company.query

def vendor_query():
    return Vendor.query

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class AddCompanyForm(FlaskForm):
    name = StringField('Company Name', validators=[DataRequired()])
    address = TextAreaField('Address', validators=[DataRequired()])
    submit = SubmitField('Add Company')

class AddVendorForm(FlaskForm):
    name = StringField('Vendor Name', validators=[DataRequired()])
    address = TextAreaField('Address', validators=[DataRequired()])
    submit = SubmitField('Add Vendor')

class AddEmployeeForm(FlaskForm):
    aadhar_card = StringField('Aadhar Card Number', validators=[DataRequired(), Length(min=12, max=12)])
    name = StringField('Full Name', validators=[DataRequired()])
    mobile_number = StringField('Mobile Number', validators=[DataRequired()])
    permanent_address = TextAreaField('Permanent Address', validators=[DataRequired()])
    present_address = TextAreaField('Present Address', validators=[DataRequired()])
    previous_job = StringField('Previous Job Title')
    duration = StringField('Duration (e.g., 2 years)')
    previous_salary = StringField('Previous Salary')
    type_of_job = StringField('Type of Job', validators=[DataRequired()])
    
    # Dropdowns for relationships
    company = QuerySelectField('Assign to Company', query_factory=company_query, allow_blank=False, get_label='name')
    vendor = QuerySelectField('Recruited Through Vendor', query_factory=vendor_query, allow_blank=True, get_label='name')
    submit = SubmitField('Add Employee')

    def validate_aadhar_card(self, aadhar_card):
        employee = Employee.query.filter_by(aadhar_card=aadhar_card.data).first()
        if employee:
            raise ValidationError('This Aadhar Card number is already registered.')