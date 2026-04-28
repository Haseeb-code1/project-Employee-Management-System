import customtkinter as ctk
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
