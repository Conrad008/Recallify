import customtkinter as ctk
 
from models import Deck
 
class DeckListView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master_app = master
 
        self.build_header()
        self.build_deck_list()

     
    def build_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=24, pady=(20, 10))
 
        welcome = ctk.CTkLabel(
            header,
            text=f"Welcome, {self.master_app.current_user.username}",
            font=ctk.CTkFont(size=22, weight="bold"),
        )
        welcome.pack(side="left")
 
        logout_btn = ctk.CTkButton(
            header, text="Log Out", width=90, fg_color="#555555",
            command=self.master_app.logout,
        )
        logout_btn.pack(side="right")
 
        new_deck_btn = ctk.CTkButton(
            header, text="+ New Deck", width=120, command=self._open_new_deck_dialog
        )
        new_deck_btn.pack(side="right", padx=(0, 10))
    