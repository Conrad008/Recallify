import customtkinter as ctk
 
from models import Card, Deck
 
 
class DeckDetail(ctk.CTkFrame):
    def __init__(self, master, deck_id: int):
        super().__init__(master)
        self.master_app = master
        self.deck_id = deck_id
        self.deck = self.master_app.session.get(Deck, deck_id)
 
        self.build_header()
        self._build_add_card_form()
        self._build_card_list()

    def build_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=24, pady=(20, 10))
 
        back_btn = ctk.CTkButton(
            header, text="< Decks", width=90, fg_color="#555555",
            command=self.master_app.show_deck_list,
        )
        back_btn.pack(side="left")
 
        title = ctk.CTkLabel(
            header, text=self.deck.name, font=ctk.CTkFont(size=22, weight="bold")
        )
        title.pack(side="left", padx=16)
 
        due_count = len(self.deck.due_cards(self.master_app.session))
        review_btn = ctk.CTkButton(
            header, text=f"Review ({due_count})", width=120,
            state="normal" if due_count else "disabled",
            fg_color="#2fa572" if due_count else "gray",
            command=lambda: self.master_app.show_review(self.deck_id),
        )
        review_btn.pack(side="right")