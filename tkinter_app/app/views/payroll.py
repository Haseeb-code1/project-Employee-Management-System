import customtkinter as ctk
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

        self.ent_emp = ctk.CTkEntry(form_frame, fg_color="#add8e6", text_color="black", placeholder_text_color="#444444", placeholder_text='Emp ID', width=120)
        self.ent_emp.grid(row=0, column=0, padx=10, pady=10)
        self.ent_salary = ctk.CTkEntry(form_frame, fg_color="#add8e6", text_color="black", placeholder_text_color="#444444", placeholder_text='Salary', width=120)
        self.ent_salary.grid(row=0, column=1, padx=10, pady=10)
        self.ent_bonus = ctk.CTkEntry(form_frame, fg_color="#add8e6", text_color="black", placeholder_text_color="#444444", placeholder_text='Bonus', width=120)
        self.ent_bonus.grid(row=0, column=2, padx=10, pady=10)
        
        self.ent_ded = ctk.CTkEntry(form_frame, fg_color="#add8e6", text_color="black", placeholder_text_color="#444444", placeholder_text='Deductions', width=120)
        self.ent_ded.grid(row=1, column=0, padx=10, pady=10)
        self.ent_my = ctk.CTkEntry(form_frame, fg_color="#add8e6", text_color="black", placeholder_text_color="#444444", placeholder_text='Month/Year', width=120)
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
