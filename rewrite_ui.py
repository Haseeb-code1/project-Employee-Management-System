import os

code_style = """import customtkinter as ctk

def setup_theme():
    ctk.set_appearance_mode('Dark')
    ctk.set_default_color_theme('blue')

def apply_treeview_style():
    from tkinter import ttk
    style = ttk.Style()
    style.theme_use('default')
    style.configure('Treeview', background='#2b2b2b', foreground='white', rowheight=30, fieldbackground='#2b2b2b', bordercolor='#343638', borderwidth=0)
    style.map('Treeview', background=[('selected', '#1f538d')])
    style.configure('Treeview.Heading', background='#1f538d', foreground='white', relief='flat', font=('Roboto', 10, 'bold'))
    style.map('Treeview.Heading', background=[('active', '#14375e')])
"""

code_main = """import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import customtkinter as ctk
from app.views.login import LoginView
from app.views.dashboard import DashboardView
from app.utils.style import setup_theme, apply_treeview_style

class EmployeeManagementApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        setup_theme()
        apply_treeview_style()
        self.title('Employee Management System')
        self.geometry('1100x700')
        self.user = None
        self.show_login()

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

    def show_login(self):
        self.clear_screen()
        self.user = None
        login_view = LoginView(self, self.on_login_success)
        login_view.pack(fill='both', expand=True)

    def on_login_success(self, user):
        self.user = user
        self.show_dashboard()

    def show_dashboard(self):
        self.clear_screen()
        dashboard_view = DashboardView(self, self.user, self.show_login)
        dashboard_view.pack(fill='both', expand=True)

if __name__ == '__main__':
    app = EmployeeManagementApp()
    app.mainloop()
"""

code_login = """import customtkinter as ctk
from app.services.auth import login
from app.utils.helpers import show_error

class LoginView(ctk.CTkFrame):
    def __init__(self, parent, on_login_success):
        super().__init__(parent)
        self.on_login_success = on_login_success
        self._build_ui()

    def _build_ui(self):
        center_frame = ctk.CTkFrame(self, corner_radius=15, width=400, height=500)
        center_frame.place(relx=0.5, rely=0.5, anchor='center')

        lbl_title = ctk.CTkLabel(center_frame, text='EMS Login', font=('Roboto', 28, 'bold'))
        lbl_title.place(relx=0.5, rely=0.15, anchor='center')

        self.ent_user = ctk.CTkEntry(center_frame, placeholder_text='Username', width=250, height=40)
        self.ent_user.place(relx=0.5, rely=0.4, anchor='center')

        self.ent_pass = ctk.CTkEntry(center_frame, placeholder_text='Password', show='*', width=250, height=40)
        self.ent_pass.place(relx=0.5, rely=0.55, anchor='center')

        btn_login = ctk.CTkButton(center_frame, text='Login', command=self.handle_login, width=250, height=40, font=('Roboto', 14, 'bold'))
        btn_login.place(relx=0.5, rely=0.75, anchor='center')

    def handle_login(self):
        username = self.ent_user.get()
        password = self.ent_pass.get()
        if not username or not password:
            show_error('Error', 'Please enter both username and password')
            return
            
        user = login(username, password)
        if user:
            self.on_login_success(user)
        else:
            show_error('Login Failed', 'Invalid username or password')
"""

code_dashboard = """import customtkinter as ctk
from app.views.employee import EmployeeView
from app.views.department import DepartmentView
from app.views.leave import LeaveView
from app.views.attendance import AttendanceView
from app.views.payroll import PayrollView
from app.views.performance import PerformanceView

class DashboardView(ctk.CTkFrame):
    def __init__(self, parent, user, on_logout):
        super().__init__(parent)
        self.user = user
        self.on_logout = on_logout
        
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.pack(side='left', fill='y')
        
        self.main_area = ctk.CTkFrame(self, corner_radius=10, fg_color='transparent')
        self.main_area.pack(side='right', fill='both', expand=True, padx=20, pady=20)

        self._build_sidebar()
        self.current_view = None
        self.show_home()

    def _build_sidebar(self):
        lbl_user = ctk.CTkLabel(self.sidebar, text=f"Welcome,\\n{self.user['username']}\\n({self.user['role']})", font=('Roboto', 16, 'bold'))
        lbl_user.pack(pady=(30, 20))

        menus = [
            ('Home', self.show_home),
            ('Employees', self.show_employees),
            ('Departments', self.show_departments),
            ('Attendance', self.show_attendance),
            ('Leaves', self.show_leaves),
            ('Payroll', self.show_payroll),
            ('Performance', self.show_performance),
            ('Logout', self.on_logout)
        ]

        for text, command in menus:
            btn = ctk.CTkButton(self.sidebar, text=text, command=command, fg_color='transparent', text_color=('gray10', 'gray90'), hover_color=('gray70', 'gray30'), anchor='w', font=('Roboto', 14))
            btn.pack(fill='x', padx=10, pady=5)

    def _clear_main_area(self):
        if self.current_view:
            self.current_view.destroy()

    def show_home(self):
        self._clear_main_area()
        self.current_view = ctk.CTkFrame(self.main_area, fg_color='transparent')
        self.current_view.pack(fill='both', expand=True)
        lbl = ctk.CTkLabel(self.current_view, text='Dashboard Home', font=('Roboto', 28, 'bold'))
        lbl.pack(pady=50)

    def show_employees(self):
        self._clear_main_area()
        self.current_view = EmployeeView(self.main_area, self.user)
        self.current_view.pack(fill='both', expand=True)

    def show_departments(self):
        self._clear_main_area()
        self.current_view = DepartmentView(self.main_area, self.user)
        self.current_view.pack(fill='both', expand=True)

    def show_attendance(self):
        self._clear_main_area()
        self.current_view = AttendanceView(self.main_area, self.user)
        self.current_view.pack(fill='both', expand=True)

    def show_leaves(self):
        self._clear_main_area()
        self.current_view = LeaveView(self.main_area, self.user)
        self.current_view.pack(fill='both', expand=True)

    def show_payroll(self):
        self._clear_main_area()
        self.current_view = PayrollView(self.main_area, self.user)
        self.current_view.pack(fill='both', expand=True)

    def show_performance(self):
        self._clear_main_area()
        self.current_view = PerformanceView(self.main_area, self.user)
        self.current_view.pack(fill='both', expand=True)
"""

code_employee = """import customtkinter as ctk
from tkinter import ttk
from app.services.employee_service import get_all_employees, add_employee, update_employee, delete_employee
from app.utils.helpers import show_error, show_info, confirm_action

class EmployeeView(ctk.CTkFrame):
    def __init__(self, parent, user):
        super().__init__(parent, fg_color='transparent')
        self.user = user
        self._build_ui()
        self.load_data()

    def _build_ui(self):
        lbl_title = ctk.CTkLabel(self, text='Employee Management', font=('Roboto', 24, 'bold'))
        lbl_title.pack(pady=(0, 20))

        form_frame = ctk.CTkFrame(self)
        form_frame.pack(fill='x', pady=10)

        self.ent_name = ctk.CTkEntry(form_frame, placeholder_text='Name', width=180)
        self.ent_name.grid(row=0, column=0, padx=10, pady=10)

        self.ent_email = ctk.CTkEntry(form_frame, placeholder_text='Email', width=180)
        self.ent_email.grid(row=0, column=1, padx=10, pady=10)

        self.ent_phone = ctk.CTkEntry(form_frame, placeholder_text='Phone', width=180)
        self.ent_phone.grid(row=0, column=2, padx=10, pady=10)

        self.ent_dept = ctk.CTkEntry(form_frame, placeholder_text='Dept ID', width=180)
        self.ent_dept.grid(row=1, column=0, padx=10, pady=10)

        self.ent_salary = ctk.CTkEntry(form_frame, placeholder_text='Salary', width=180)
        self.ent_salary.grid(row=1, column=1, padx=10, pady=10)

        btn_frame = ctk.CTkFrame(self, fg_color='transparent')
        btn_frame.pack(fill='x', pady=10)

        if self.user['role'] in ['Admin', 'HR']:
            ctk.CTkButton(btn_frame, text='Add', command=self.add_emp, width=100).pack(side='left', padx=10)
            ctk.CTkButton(btn_frame, text='Update', command=self.update_emp, width=100, fg_color='#E67E22', hover_color='#D35400').pack(side='left', padx=10)
            ctk.CTkButton(btn_frame, text='Delete', command=self.delete_emp, width=100, fg_color='#E74C3C', hover_color='#C0392B').pack(side='left', padx=10)

        columns = ('id', 'name', 'email', 'phone', 'department', 'salary')
        self.tree = ttk.Treeview(self, columns=columns, show='headings', height=10)
        for col in columns:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=120, anchor='center')
        self.tree.pack(fill='both', expand=True, pady=10)
        self.tree.bind('<Double-1>', self.on_select)

    def load_data(self):
        for item in self.tree.get_children(): self.tree.delete(item)
        for emp in get_all_employees():
            self.tree.insert('', 'end', values=(emp['id'], emp['name'], emp['email'], emp['phone'], emp['department'], emp['salary']))

    def on_select(self, event):
        selected = self.tree.selection()
        if not selected: return
        item = self.tree.item(selected[0])['values']
        self.ent_name.delete(0, 'end')
        self.ent_name.insert(0, item[1])
        self.ent_email.delete(0, 'end')
        self.ent_email.insert(0, item[2])
        self.ent_phone.delete(0, 'end')
        self.ent_phone.insert(0, item[3])
        self.ent_dept.delete(0, 'end')
        self.ent_salary.delete(0, 'end')
        self.ent_salary.insert(0, item[5])

    def add_emp(self):
        try:
            add_employee(self.ent_name.get(), self.ent_email.get(), self.ent_phone.get(), self.ent_dept.get(), self.ent_salary.get())
            self.load_data()
        except Exception as e:
            show_error('Error', str(e))

    def update_emp(self):
        selected = self.tree.selection()
        if not selected: return
        try:
            update_employee(self.tree.item(selected[0])['values'][0], self.ent_name.get(), self.ent_email.get(), self.ent_phone.get(), self.ent_dept.get(), self.ent_salary.get())
            self.load_data()
        except Exception as e:
            show_error('Error', str(e))

    def delete_emp(self):
        selected = self.tree.selection()
        if not selected: return
        if confirm_action('Confirm', 'Delete?'):
            try:
                delete_employee(self.tree.item(selected[0])['values'][0])
                self.load_data()
            except Exception as e:
                show_error('Error', str(e))
"""

code_dept = """import customtkinter as ctk
from tkinter import ttk
from app.services.department_service import get_all_departments, add_department, update_department, delete_department
from app.utils.helpers import show_error, show_info, confirm_action

class DepartmentView(ctk.CTkFrame):
    def __init__(self, parent, user):
        super().__init__(parent, fg_color='transparent')
        self.user = user
        self._build_ui()
        self.load_data()

    def _build_ui(self):
        lbl_title = ctk.CTkLabel(self, text='Department Management', font=('Roboto', 24, 'bold'))
        lbl_title.pack(pady=(0, 20))

        form_frame = ctk.CTkFrame(self)
        form_frame.pack(fill='x', pady=10)

        self.ent_name = ctk.CTkEntry(form_frame, placeholder_text='Department Name', width=300)
        self.ent_name.pack(side='left', padx=20, pady=20)

        btn_frame = ctk.CTkFrame(self, fg_color='transparent')
        btn_frame.pack(fill='x', pady=10)

        if self.user['role'] == 'Admin':
            ctk.CTkButton(btn_frame, text='Add', command=self.add_dept, width=100).pack(side='left', padx=10)
            ctk.CTkButton(btn_frame, text='Update', command=self.update_dept, width=100, fg_color='#E67E22', hover_color='#D35400').pack(side='left', padx=10)
            ctk.CTkButton(btn_frame, text='Delete', command=self.delete_dept, width=100, fg_color='#E74C3C', hover_color='#C0392B').pack(side='left', padx=10)

        columns = ('id', 'name')
        self.tree = ttk.Treeview(self, columns=columns, show='headings', height=10)
        for col in columns: self.tree.heading(col, text=col.capitalize())
        self.tree.pack(fill='both', expand=True, pady=10)
        self.tree.bind('<Double-1>', self.on_select)

    def load_data(self):
        for item in self.tree.get_children(): self.tree.delete(item)
        for dept in get_all_departments(): self.tree.insert('', 'end', values=(dept['id'], dept['name']))

    def on_select(self, event):
        selected = self.tree.selection()
        if not selected: return
        item = self.tree.item(selected[0])['values']
        self.ent_name.delete(0, 'end')
        self.ent_name.insert(0, item[1])

    def add_dept(self):
        try:
            add_department(self.ent_name.get())
            self.load_data()
        except Exception as e:
            show_error('Error', str(e))

    def update_dept(self):
        selected = self.tree.selection()
        if not selected: return
        try:
            update_department(self.tree.item(selected[0])['values'][0], self.ent_name.get())
            self.load_data()
        except Exception as e:
            show_error('Error', str(e))

    def delete_dept(self):
        selected = self.tree.selection()
        if not selected: return
        if confirm_action('Confirm', 'Delete department?'):
            try:
                delete_department(self.tree.item(selected[0])['values'][0])
                self.load_data()
            except Exception as e:
                show_error('Error', str(e))
"""

code_attendance = """import customtkinter as ctk
from tkinter import ttk
from app.services.attendance_service import get_attendance, add_attendance
from app.utils.helpers import show_error

class AttendanceView(ctk.CTkFrame):
    def __init__(self, parent, user):
        super().__init__(parent, fg_color='transparent')
        self.user = user
        self._build_ui()
        self.load_data()

    def _build_ui(self):
        lbl_title = ctk.CTkLabel(self, text='Attendance', font=('Roboto', 24, 'bold'))
        lbl_title.pack(pady=(0, 20))

        form_frame = ctk.CTkFrame(self)
        form_frame.pack(fill='x', pady=10)

        self.ent_emp = ctk.CTkEntry(form_frame, placeholder_text='Emp ID', width=150)
        self.ent_emp.pack(side='left', padx=10, pady=10)

        self.ent_date = ctk.CTkEntry(form_frame, placeholder_text='Date YYYY-MM-DD', width=150)
        self.ent_date.pack(side='left', padx=10, pady=10)

        self.ent_status = ctk.CTkComboBox(form_frame, values=['Present', 'Absent', 'Half Day', 'Leave'], width=150)
        self.ent_status.pack(side='left', padx=10, pady=10)

        ctk.CTkButton(form_frame, text='Mark', command=self.add, width=100).pack(side='left', padx=10, pady=10)

        columns = ('id', 'employee', 'date', 'status')
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        for col in columns: self.tree.heading(col, text=col.capitalize())
        self.tree.pack(fill='both', expand=True, pady=10)

    def load_data(self):
        for item in self.tree.get_children(): self.tree.delete(item)
        for row in get_attendance(): self.tree.insert('', 'end', values=(row['id'], row['name'], row['date'], row['status']))

    def add(self):
        try:
            add_attendance(self.ent_emp.get(), self.ent_date.get(), self.ent_status.get())
            self.load_data()
        except Exception as e:
            show_error('Error', str(e))
"""

code_leave = """import customtkinter as ctk
from tkinter import ttk
from app.services.leave_service import get_all_leaves, apply_leave, update_leave_status
from app.utils.helpers import show_error

class LeaveView(ctk.CTkFrame):
    def __init__(self, parent, user):
        super().__init__(parent, fg_color='transparent')
        self.user = user
        self._build_ui()
        self.load_data()

    def _build_ui(self):
        lbl_title = ctk.CTkLabel(self, text='Leave Management', font=('Roboto', 24, 'bold'))
        lbl_title.pack(pady=(0, 20))

        form_frame = ctk.CTkFrame(self)
        form_frame.pack(fill='x', pady=10)

        self.ent_emp = ctk.CTkEntry(form_frame, placeholder_text='Emp ID', width=120)
        self.ent_emp.grid(row=0, column=0, padx=10, pady=10)

        self.ent_start = ctk.CTkEntry(form_frame, placeholder_text='Start Date', width=120)
        self.ent_start.grid(row=0, column=1, padx=10, pady=10)

        self.ent_end = ctk.CTkEntry(form_frame, placeholder_text='End Date', width=120)
        self.ent_end.grid(row=0, column=2, padx=10, pady=10)

        ctk.CTkButton(form_frame, text='Apply', command=self.apply, width=100).grid(row=0, column=3, padx=10, pady=10)

        if self.user['role'] in ['Admin', 'HR']:
            btn_frame = ctk.CTkFrame(self, fg_color='transparent')
            btn_frame.pack(fill='x', pady=5)
            ctk.CTkButton(btn_frame, text='Approve', command=lambda: self.update_status('Approved'), fg_color='#27AE60', hover_color='#2ECC71').pack(side='left', padx=10)
            ctk.CTkButton(btn_frame, text='Reject', command=lambda: self.update_status('Rejected'), fg_color='#C0392B', hover_color='#E74C3C').pack(side='left', padx=10)

        columns = ('id', 'employee', 'start_date', 'end_date', 'status')
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        for col in columns: self.tree.heading(col, text=col.capitalize())
        self.tree.pack(fill='both', expand=True, pady=10)

    def load_data(self):
        for item in self.tree.get_children(): self.tree.delete(item)
        for row in get_all_leaves(): self.tree.insert('', 'end', values=(row['id'], row['name'], row['start_date'], row['end_date'], row['status']))

    def apply(self):
        try:
            apply_leave(self.ent_emp.get(), self.ent_start.get(), self.ent_end.get())
            self.load_data()
        except Exception as e:
            show_error('Error', str(e))

    def update_status(self, status):
        selected = self.tree.selection()
        if not selected: return
        leave_id = self.tree.item(selected[0])['values'][0]
        try:
            update_leave_status(leave_id, status)
            self.load_data()
        except Exception as e:
            show_error('Error', str(e))
"""

code_payroll = """import customtkinter as ctk
from tkinter import ttk
from app.services.payroll_service import get_all_payroll, add_payroll
from app.utils.helpers import show_error

class PayrollView(ctk.CTkFrame):
    def __init__(self, parent, user):
        super().__init__(parent, fg_color='transparent')
        self.user = user
        self._build_ui()
        self.load_data()

    def _build_ui(self):
        lbl_title = ctk.CTkLabel(self, text='Payroll Management', font=('Roboto', 24, 'bold'))
        lbl_title.pack(pady=(0, 20))

        form_frame = ctk.CTkFrame(self)
        form_frame.pack(fill='x', pady=10)

        self.ent_emp = ctk.CTkEntry(form_frame, placeholder_text='Emp ID', width=120)
        self.ent_emp.grid(row=0, column=0, padx=10, pady=10)
        self.ent_salary = ctk.CTkEntry(form_frame, placeholder_text='Salary', width=120)
        self.ent_salary.grid(row=0, column=1, padx=10, pady=10)
        self.ent_bonus = ctk.CTkEntry(form_frame, placeholder_text='Bonus', width=120)
        self.ent_bonus.grid(row=0, column=2, padx=10, pady=10)
        
        self.ent_ded = ctk.CTkEntry(form_frame, placeholder_text='Deductions', width=120)
        self.ent_ded.grid(row=1, column=0, padx=10, pady=10)
        self.ent_my = ctk.CTkEntry(form_frame, placeholder_text='Month/Year', width=120)
        self.ent_my.grid(row=1, column=1, padx=10, pady=10)

        ctk.CTkButton(form_frame, text='Add', command=self.add, width=100).grid(row=1, column=2, padx=10, pady=10)

        columns = ('id', 'employee', 'salary', 'bonus', 'deductions', 'month_year')
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        for col in columns: self.tree.heading(col, text=col.capitalize())
        self.tree.pack(fill='both', expand=True, pady=10)

    def load_data(self):
        for item in self.tree.get_children(): self.tree.delete(item)
        for row in get_all_payroll(): self.tree.insert('', 'end', values=(row['id'], row['name'], row['salary'], row['bonus'], row['deductions'], row['month_year']))

    def add(self):
        try:
            add_payroll(self.ent_emp.get(), self.ent_salary.get(), self.ent_bonus.get(), self.ent_ded.get(), self.ent_my.get())
            self.load_data()
        except Exception as e:
            show_error('Error', str(e))
"""

code_performance = """import customtkinter as ctk
from tkinter import ttk
from app.services.performance_service import get_all_performance, add_performance
from app.utils.helpers import show_error

class PerformanceView(ctk.CTkFrame):
    def __init__(self, parent, user):
        super().__init__(parent, fg_color='transparent')
        self.user = user
        self._build_ui()
        self.load_data()

    def _build_ui(self):
        lbl_title = ctk.CTkLabel(self, text='Performance Evaluation', font=('Roboto', 24, 'bold'))
        lbl_title.pack(pady=(0, 20))

        form_frame = ctk.CTkFrame(self)
        form_frame.pack(fill='x', pady=10)

        self.ent_emp = ctk.CTkEntry(form_frame, placeholder_text='Emp ID', width=120)
        self.ent_emp.grid(row=0, column=0, padx=10, pady=10)
        self.ent_rating = ctk.CTkEntry(form_frame, placeholder_text='Rating (1-5)', width=120)
        self.ent_rating.grid(row=0, column=1, padx=10, pady=10)
        self.ent_date = ctk.CTkEntry(form_frame, placeholder_text='Date', width=120)
        self.ent_date.grid(row=0, column=2, padx=10, pady=10)
        
        self.ent_fb = ctk.CTkEntry(form_frame, placeholder_text='Feedback', width=260)
        self.ent_fb.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        ctk.CTkButton(form_frame, text='Add', command=self.add, width=100).grid(row=1, column=2, padx=10, pady=10)

        columns = ('id', 'employee', 'rating', 'feedback', 'date')
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        for col in columns: self.tree.heading(col, text=col.capitalize())
        self.tree.pack(fill='both', expand=True, pady=10)

    def load_data(self):
        for item in self.tree.get_children(): self.tree.delete(item)
        for row in get_all_performance(): self.tree.insert('', 'end', values=(row['id'], row['name'], row['rating'], row['feedback'], row['date']))

    def add(self):
        try:
            add_performance(self.ent_emp.get(), self.ent_rating.get(), self.ent_fb.get(), self.ent_date.get())
            self.load_data()
        except Exception as e:
            show_error('Error', str(e))
"""

with open('tkinter_app/app/utils/style.py', 'w') as f: f.write(code_style)
with open('tkinter_app/app/main.py', 'w') as f: f.write(code_main)
with open('tkinter_app/app/views/login.py', 'w') as f: f.write(code_login)
with open('tkinter_app/app/views/dashboard.py', 'w') as f: f.write(code_dashboard)
with open('tkinter_app/app/views/employee.py', 'w') as f: f.write(code_employee)
with open('tkinter_app/app/views/department.py', 'w') as f: f.write(code_dept)
with open('tkinter_app/app/views/attendance.py', 'w') as f: f.write(code_attendance)
with open('tkinter_app/app/views/leave.py', 'w') as f: f.write(code_leave)
with open('tkinter_app/app/views/payroll.py', 'w') as f: f.write(code_payroll)
with open('tkinter_app/app/views/performance.py', 'w') as f: f.write(code_performance)
