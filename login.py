import customtkinter as ctk
 
from auth import login_user, register_user, AuthError

class LoginView(ctk.CTkFrame):
    def __init__(self, master, on_login_success):
        super().__init__(master)
        self.master_app = master
        self.on_login_success = on_login_success
 
        self.mode = "login"  
 
        self._build_ui()