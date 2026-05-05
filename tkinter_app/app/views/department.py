import customtkinter as ctk
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

        self.ent_name = ctk.CTkEntry(form_frame, fg_color="#add8e6", text_color="black", placeholder_text_color="#444444", placeholder_text='Department Name', width=300)
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
