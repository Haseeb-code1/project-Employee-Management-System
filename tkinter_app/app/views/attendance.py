import customtkinter as ctk
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
