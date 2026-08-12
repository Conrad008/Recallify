from datetime import date
 
import customtkinter as ctk
 
from models import Deck, ReviewLog
from scheduler import SpacedRepetitionScheduler

QUALITY_LABELS = {
    0: "Blackout",
    1: "Wrong",
    2: "Close",
    3: "Hard",
    4: "Good",
    5: "Easy",
}
QUALITY_COLORS = {
    0: "#c0392b",
    1: "#e74c3c",
    2: "#e67e22",
    3: "#f1c40f",
    4: "#2ecc71",
    5: "#27ae60",
}
  
class ReviewView(ctk.CTkFrame):
    def __init__(self, master, deck_id: int):
        super().__init__(master)
        self.master_app = master
        self.deck_id = deck_id
        self.deck = self.master_app.session.get(Deck, deck_id)
 
        self.queue = self.deck.due_cards(self.master_app.session)
        self.total_due = len(self.queue)
        self.reviewed_count = 0
        self.showing_answer = False
 
        self._build_ui()
        self._load_next_card()