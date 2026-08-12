import customtkinter as ctk
 
from models import Card, Deck
 
 
class DeckDetail(ctk.CTkFrame):
    def __init__(self, master, deck_id: int):
        super().__init__(master)
        self.master_app = master
        self.deck_id = deck_id
        self.deck = self.master_app.session.get(Deck, deck_id)
 
        self._build_header()
        self._build_add_card_form()
        self._build_card_list()
 