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

    def build_deck_list(self):
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True, padx=24, pady=10)
 
        self._refresh_decks()
 
    def refresh_decks(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
 
        user = self.master_app.current_user
        decks = user.decks
 
        if not decks:
            empty_label = ctk.CTkLabel(
                self.scroll_frame,
                text="No decks yet. Click '+ New Deck' to create your first one.",
                text_color="gray",
            )
            empty_label.pack(pady=40)
            return
 
        for deck in decks:
            self._build_deck_card(deck)