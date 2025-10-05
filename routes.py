from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from urllib.parse import urlparse 
from app import app, db
from forms import LoginForm, AddCompanyForm, AddVendorForm, AddEmployeeForm
from models import User, Company, Vendor, Employee

@app.route('/')
@app.route('/index')
def index():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin_dashboard'))
        elif current_user.role == 'company':
            return redirect(url_for('company_dashboard'))
        elif current_user.role == 'vendor':
            return redirect(url_for('vendor_dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=True)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

# --- Admin Routes ---
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('index'))
    companies = Company.query.all()
    vendors = Vendor.query.all()
    employees = Employee.query.all()
    return render_template('admin/dashboard.html', companies=companies, vendors=vendors, employees=employees)

@app.route('/admin/add_company', methods=['GET', 'POST'])
@login_required
def add_company():
    if current_user.role != 'admin':
        return redirect(url_for('index'))
    form = AddCompanyForm()
    if form.validate_on_submit():
        username = form.name.data.lower().replace(' ', '') + '_company'
        user = User(username=username, role='company')
        user.set_password(app.config['DEFAULT_PASSWORD'])
        db.session.add(user)
        
        company = Company(name=form.name.data, address=form.address.data, user=user)
        db.session.add(company)
        db.session.commit()
        flash(f'Company {form.name.data} and user {username} created!', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin/add_company.html', form=form)

@app.route('/admin/add_vendor', methods=['GET', 'POST'])
@login_required
def add_vendor():
    if current_user.role != 'admin':
        return redirect(url_for('index'))
    form = AddVendorForm()
    if form.validate_on_submit():
        username = form.name.data.lower().replace(' ', '') + '_vendor'
        user = User(username=username, role='vendor')
        user.set_password(app.config['DEFAULT_PASSWORD'])
        db.session.add(user)

        vendor = Vendor(name=form.name.data, address=form.address.data, user=user)
        db.session.add(vendor)
        db.session.commit()
        flash(f'Vendor {form.name.data} and user {username} created!', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin/add_vendor.html', form=form)


# --- Company Routes ---
@app.route('/company/dashboard')
@login_required
def company_dashboard():
    if current_user.role != 'company':
        return redirect(url_for('index'))
    company = current_user.company
    employees = company.employees.all()
    return render_template('company/dashboard.html', company=company, employees=employees)

@app.route('/company/add_employee', methods=['GET', 'POST'])
@login_required
def company_add_employee():
    if current_user.role != 'company':
        return redirect(url_for('index'))
    form = AddEmployeeForm()
    # The company is fixed for this user
    form.company.data = current_user.company
    if form.validate_on_submit():
        employee = Employee(
            aadhar_card=form.aadhar_card.data,
            name=form.name.data,
            mobile_number=form.mobile_number.data,
            permanent_address=form.permanent_address.data,
            present_address=form.present_address.data,
            previous_job=form.previous_job.data,
            duration=form.duration.data,
            previous_salary=form.previous_salary.data,
            type_of_job=form.type_of_job.data,
            company=current_user.company,
            vendor=form.vendor.data
        )
        db.session.add(employee)
        db.session.commit()
        flash('Employee added successfully!', 'success')
        return redirect(url_for('company_dashboard'))
    return render_template('company/add_employee.html', form=form)

# --- Vendor Routes ---
@app.route('/vendor/dashboard')
@login_required
def vendor_dashboard():
    if current_user.role != 'vendor':
        return redirect(url_for('index'))
    vendor = current_user.vendor
    employees = vendor.employees.all()
    return render_template('vendor/dashboard.html', vendor=vendor, employees=employees)

@app.route('/vendor/add_employee', methods=['GET', 'POST'])
@login_required
def vendor_add_employee():
    if current_user.role != 'vendor':
        return redirect(url_for('index'))
    form = AddEmployeeForm()
    # Pre-fill and fix the vendor field
    form.vendor.data = current_user.vendor
    if form.validate_on_submit():
        employee = Employee(
            aadhar_card=form.aadhar_card.data,
            name=form.name.data,
            mobile_number=form.mobile_number.data,
            permanent_address=form.permanent_address.data,
            present_address=form.present_address.data,
            previous_job=form.previous_job.data,
            duration=form.duration.data,
            previous_salary=form.previous_salary.data,
            type_of_job=form.type_of_job.data,
            company=form.company.data,
            vendor=current_user.vendor # Ensure vendor is set to the current user
        )
        db.session.add(employee)
        db.session.commit()
        flash('Employee added successfully!', 'success')
        return redirect(url_for('vendor_dashboard'))
    return render_template('vendor/add_employee.html', form=form)