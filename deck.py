import customtkinter as ctk
 
from models import Deck
 
class DeckListView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master_app = master
 
        self._build_header()
        self._build_deck_list()
