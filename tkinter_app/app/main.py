import sys
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
