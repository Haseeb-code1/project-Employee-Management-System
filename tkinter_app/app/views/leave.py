import customtkinter as ctk
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

        self.ent_emp = ctk.CTkEntry(form_frame, fg_color="#add8e6", text_color="black", placeholder_text_color="#444444", placeholder_text='Emp ID', width=120)
        self.ent_emp.grid(row=0, column=0, padx=10, pady=10)

        self.ent_start = ctk.CTkEntry(form_frame, fg_color="#add8e6", text_color="black", placeholder_text_color="#444444", placeholder_text='Start Date', width=120)
        self.ent_start.grid(row=0, column=1, padx=10, pady=10)

        self.ent_end = ctk.CTkEntry(form_frame, fg_color="#add8e6", text_color="black", placeholder_text_color="#444444", placeholder_text='End Date', width=120)
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
