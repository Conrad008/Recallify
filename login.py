import customtkinter as ctk
 
from auth import login_user, register_user, AuthError

class LoginView(ctk.CTkFrame):
    def __init__(self, master, on_login_success):
        super().__init__(master)
        self.master_app = master
        self.on_login_success = on_login_success
 
        self.mode = "login"  
 
        self._build_ui()

    def _build_ui(self):
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.place(relx=0.5, rely=0.5, anchor="center")
 
        self.title_label = ctk.CTkLabel(
            container, text="SpacedCards", font=ctk.CTkFont(size=28, weight="bold")
        )
        self.title_label.pack(pady=(0, 4))
 
        self.subtitle_label = ctk.CTkLabel(
            container, text="Log in to your account", font=ctk.CTkFont(size=14)
        )
        self.subtitle_label.pack(pady=(0, 20))
 
        self.username_entry = ctk.CTkEntry(container, placeholder_text="Username", width=280)
        self.username_entry.pack(pady=6)
 
        self.password_entry = ctk.CTkEntry(
            container, placeholder_text="Password", show="*", width=280
        )
        self.password_entry.pack(pady=6)
        self.password_entry.bind("<Return>", lambda event: self._on_submit())
 
        self.error_label = ctk.CTkLabel(container, text="", text_color="#e74c3c")
        self.error_label.pack(pady=(8, 0))
 
        self.submit_button = ctk.CTkButton(
            container, text="Log In", width=280, command=self._on_submit
        )
        self.submit_button.pack(pady=(12, 6))
 
        self.toggle_button = ctk.CTkButton(
            container,
            text="Don't have an account? Create one",
            width=280,
            fg_color="transparent",
            hover_color=("#dddddd", "#333333"),
            command=self._toggle_mode,
        )
        self.toggle_button.pack(pady=(0, 4))