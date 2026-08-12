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
 
        self.build_ui()
        self.load_next_card()

    def build_ui(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=24, pady=(20, 10))
 
        back_btn = ctk.CTkButton(
            header, text="< Back to Deck", width=120, fg_color="#555555",
            command=lambda: self.master_app.show_deck_detail(self.deck_id),
        )
        back_btn.pack(side="left")
 
        self.progress_label = ctk.CTkLabel(header, text="", font=ctk.CTkFont(size=14))
        self.progress_label.pack(side="right")
 
        self.card_frame = ctk.CTkFrame(self, corner_radius=14)
        self.card_frame.pack(fill="both", expand=True, padx=40, pady=10)
 
        self.front_label = ctk.CTkLabel(
            self.card_frame, text="", font=ctk.CTkFont(size=24, weight="bold"),
            wraplength=600, justify="center",
        )
        self.front_label.place(relx=0.5, rely=0.35, anchor="center")
 
        self.back_label = ctk.CTkLabel(
            self.card_frame, text="", font=ctk.CTkFont(size=20),
            text_color="#2fa572", wraplength=600, justify="center",
        )
        self.back_label.place(relx=0.5, rely=0.6, anchor="center")
 
        self.controls_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.controls_frame.pack(fill="x", padx=40, pady=(0, 24))
 
        self.show_answer_btn = ctk.CTkButton(
            self.controls_frame, text="Show Answer", width=200, height=44,
            font=ctk.CTkFont(size=15, weight="bold"),
            command=self._on_show_answer,
        )
 
        self.rating_buttons_frame = ctk.CTkFrame(self.controls_frame, fg_color="transparent")
        self.rating_buttons = []
        for quality in range(6):
            btn = ctk.CTkButton(
                self.rating_buttons_frame,
                text=f"{quality}\n{QUALITY_LABELS[quality]}",
                width=90, height=54,
                fg_color=QUALITY_COLORS[quality],
                hover_color=QUALITY_COLORS[quality],
                command=lambda q=quality: self._on_rate(q),
            )
            btn.pack(side="left", padx=6)
            self.rating_buttons.append(btn)

    def load_next_card(self):
        self.showing_answer = False
        self.back_label.configure(text="")
        self.rating_buttons_frame.pack_forget()
 
        if not self.queue:
            self._show_session_complete()
            return
 
        self.current_card = self.queue[0]
        self.front_label.configure(text=self.current_card.front_text)
        self.progress_label.configure(
            text=f"Card {self.reviewed_count + 1} of {self.total_due}"
        )
        self.show_answer_btn.pack(pady=8)
 
    def _on_show_answer(self):
        self.showing_answer = True
        self.back_label.configure(text=self.current_card.back_text)
        self.show_answer_btn.pack_forget()
        self.rating_buttons_frame.pack(pady=8)
 
    def _on_rate(self, quality: int):
        card = self.current_card
        session = self.master_app.session
 
        interval_before = card.interval
        easiness_before = card.easiness_factor
 
        result = SpacedRepetitionScheduler.calculate_next_review(
            quality_rating=quality,
            easiness_factor=card.easiness_factor,
            repetitions=card.repetitions,
            interval=card.interval,
            today=date.today(),
        )
 
        card.easiness_factor = result.easiness_factor
        card.repetitions = result.repetitions
        card.interval = result.interval
        card.next_review_date = result.next_review_date
 
        log = ReviewLog(
            card_id=card.id,
            quality_rating=quality,
            interval_before=interval_before,
            interval_after=result.interval,
            easiness_before=easiness_before,
            easiness_after=result.easiness_factor,
        )
        session.add(log)
        session.commit()
 
        self.reviewed_count += 1
        self.queue.pop(0)
        self.load_next_card()
 
    def _show_session_complete(self):
        self.front_label.configure(text="All done for now! 🎉")
        self.progress_label.configure(text=f"Reviewed {self.reviewed_count} card(s)")
        self.show_answer_btn.pack_forget()
        self.rating_buttons_frame.pack_forget()
 
        done_btn = ctk.CTkButton(
            self.controls_frame, text="Back to Deck", width=200, height=44,
            command=lambda: self.master_app.show_deck_detail(self.deck_id),
        )
        done_btn.pack(pady=8)
 