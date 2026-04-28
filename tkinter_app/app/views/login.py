import customtkinter as ctk
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
