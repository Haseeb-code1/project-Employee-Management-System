import customtkinter as ctk
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

        self.ent_name = ctk.CTkEntry(form_frame, fg_color="#add8e6", text_color="black", placeholder_text_color="#444444", placeholder_text='Name', width=180)
        self.ent_name.grid(row=0, column=0, padx=10, pady=10)

        self.ent_email = ctk.CTkEntry(form_frame, fg_color="#add8e6", text_color="black", placeholder_text_color="#444444", placeholder_text='Email', width=180)
        self.ent_email.grid(row=0, column=1, padx=10, pady=10)

        self.ent_phone = ctk.CTkEntry(form_frame, fg_color="#add8e6", text_color="black", placeholder_text_color="#444444", placeholder_text='Phone', width=180)
        self.ent_phone.grid(row=0, column=2, padx=10, pady=10)

        self.ent_dept = ctk.CTkEntry(form_frame, fg_color="#add8e6", text_color="black", placeholder_text_color="#444444", placeholder_text='Dept ID', width=180)
        self.ent_dept.grid(row=1, column=0, padx=10, pady=10)

        self.ent_salary = ctk.CTkEntry(form_frame, fg_color="#add8e6", text_color="black", placeholder_text_color="#444444", placeholder_text='Salary', width=180)
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
