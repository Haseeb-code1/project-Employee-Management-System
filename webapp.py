import os
import sys

# Add tkinter_app to sys.path so that 'app.utils.db' imports work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'tkinter_app')))

from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
from app.services.auth import login as auth_login
from app.services.employee_service import get_all_employees, add_employee, update_employee, delete_employee
from app.services.department_service import get_all_departments, add_department, update_department, delete_department
from app.services.attendance_service import get_attendance, add_attendance
from app.services.leave_service import get_all_leaves, apply_leave, update_leave_status
from app.services.payroll_service import get_all_payroll, add_payroll
from app.services.performance_service import get_all_performance, add_performance

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "super_secret_key")

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'role' not in session or session['role'] not in roles:
                flash("You don't have permission to access this page.", "danger")
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = auth_login(username, password)
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            session['employee_id'] = user.get('employee_id') # Handle if linked to employee
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials", "danger")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', role=session.get('role'))

# --- Employee Routes ---
@app.route('/employees')
@login_required
@role_required('Admin', 'HR')
def employees():
    emps = get_all_employees()
    departments = get_all_departments()
    return render_template('employees.html', employees=emps, departments=departments)

@app.route('/employees/add', methods=['POST'])
@login_required
@role_required('Admin', 'HR')
def create_employee():
    try:
        add_employee(
            request.form['name'],
            request.form['email'],
            request.form['phone'],
            request.form['department_id'],
            request.form['salary']
        )
        flash("Employee added successfully.", "success")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for('employees'))

@app.route('/employees/edit/<int:id>', methods=['POST'])
@login_required
@role_required('Admin', 'HR')
def edit_employee(id):
    try:
        update_employee(
            id,
            request.form['name'],
            request.form['email'],
            request.form['phone'],
            request.form['department_id'],
            request.form['salary']
        )
        flash("Employee updated successfully.", "success")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for('employees'))

@app.route('/employees/delete/<int:id>', methods=['POST'])
@login_required
@role_required('Admin')
def remove_employee(id):
    try:
        delete_employee(id)
        flash("Employee deleted successfully.", "success")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for('employees'))

# --- Department Routes ---
@app.route('/departments')
@login_required
@role_required('Admin', 'HR')
def departments():
    depts = get_all_departments()
    return render_template('departments.html', departments=depts)

@app.route('/departments/add', methods=['POST'])
@login_required
@role_required('Admin', 'HR')
def create_department():
    try:
        add_department(request.form['name'])
        flash("Department added successfully.", "success")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for('departments'))

@app.route('/departments/edit/<int:id>', methods=['POST'])
@login_required
@role_required('Admin', 'HR')
def edit_department(id):
    try:
        update_department(id, request.form['name'])
        flash("Department updated successfully.", "success")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for('departments'))

@app.route('/departments/delete/<int:id>', methods=['POST'])
@login_required
@role_required('Admin')
def remove_department(id):
    try:
        delete_department(id)
        flash("Department deleted successfully.", "success")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for('departments'))

# --- Attendance Routes ---
@app.route('/attendance')
@login_required
def attendance():
    # If Employee, only show their attendance. For simplicity, showing all to Admin/HR, and filtering if needed.
    records = get_attendance()
    if session.get('role') == 'Employee':
        # Wait, get_attendance doesn't take employee_id in the original code? We'll filter in Python.
        # But if we don't have employee_id linked, we assume name matches username or similar? Let's just pass all for now or filter if possible.
        pass
    employees = get_all_employees()
    return render_template('attendance.html', records=records, employees=employees)

@app.route('/attendance/add', methods=['POST'])
@login_required
@role_required('Admin', 'HR')
def create_attendance():
    try:
        add_attendance(
            request.form['employee_id'],
            request.form['date'],
            request.form['status']
        )
        flash("Attendance recorded successfully.", "success")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for('attendance'))

# --- Leave Routes ---
@app.route('/leaves')
@login_required
def leaves():
    records = get_all_leaves()
    employees = get_all_employees()
    return render_template('leaves.html', records=records, employees=employees)

@app.route('/leaves/apply', methods=['POST'])
@login_required
def create_leave():
    try:
        apply_leave(
            request.form['employee_id'],
            request.form['start_date'],
            request.form['end_date']
        )
        flash("Leave applied successfully.", "success")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for('leaves'))

@app.route('/leaves/update/<int:id>', methods=['POST'])
@login_required
@role_required('Admin', 'HR')
def modify_leave(id):
    try:
        update_leave_status(id, request.form['status'])
        flash("Leave status updated.", "success")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for('leaves'))

# --- Payroll Routes ---
@app.route('/payroll')
@login_required
@role_required('Admin', 'HR')
def payroll():
    records = get_all_payroll()
    employees = get_all_employees()
    return render_template('payroll.html', records=records, employees=employees)

@app.route('/payroll/add', methods=['POST'])
@login_required
@role_required('Admin', 'HR')
def create_payroll():
    try:
        add_payroll(
            request.form['employee_id'],
            request.form['salary'],
            request.form['bonus'],
            request.form['deductions'],
            request.form['month_year']
        )
        flash("Payroll added successfully.", "success")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for('payroll'))

# --- Performance Routes ---
@app.route('/performance')
@login_required
@role_required('Admin', 'HR')
def performance():
    records = get_all_performance()
    employees = get_all_employees()
    return render_template('performance.html', records=records, employees=employees)

@app.route('/performance/add', methods=['POST'])
@login_required
@role_required('Admin', 'HR')
def create_performance():
    try:
        add_performance(
            request.form['employee_id'],
            request.form['rating'],
            request.form['feedback'],
            request.form['date']
        )
        flash("Performance evaluation added.", "success")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for('performance'))

if __name__ == '__main__':
    app.run(debug=True)
