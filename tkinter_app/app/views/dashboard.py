import customtkinter as ctk
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
        lbl_user = ctk.CTkLabel(self.sidebar, text=f"Welcome,\n{self.user['username']}\n({self.user['role']})", font=('Roboto', 16, 'bold'))
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
