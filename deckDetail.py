import customtkinter as ctk
 
from models import Card, Deck
 
 
class DeckDetail(ctk.CTkFrame):
    def __init__(self, master, deck_id: int):
        super().__init__(master)
        self.master_app = master
        self.deck_id = deck_id
        self.deck = self.master_app.session.get(Deck, deck_id)
 
        self.build_header()
        self.build_add_card_form()
        self.build_card_list()

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

    def build_add_card_form(self):
        form = ctk.CTkFrame(self, corner_radius=10)
        form.pack(fill="x", padx=24, pady=(0, 12))
 
        form_label = ctk.CTkLabel(
            form, text="Add a Card", font=ctk.CTkFont(size=14, weight="bold")
        )
        form_label.pack(anchor="w", padx=16, pady=(12, 4))
 
        entry_row = ctk.CTkFrame(form, fg_color="transparent")
        entry_row.pack(fill="x", padx=16, pady=(0, 12))
 
        self.front_entry = ctk.CTkEntry(entry_row, placeholder_text="Front (question)")
        self.front_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
 
        self.back_entry = ctk.CTkEntry(entry_row, placeholder_text="Back (answer)")
        self.back_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.back_entry.bind("<Return>", lambda e: self._on_add_card())
 
        add_btn = ctk.CTkButton(entry_row, text="Add", width=80, command=self.on_add_card)
        add_btn.pack(side="left")
 
        self.form_error_label = ctk.CTkLabel(form, text="", text_color="#e74c3c")
        self.form_error_label.pack(anchor="w", padx=16, pady=(0, 8))

    def on_add_card(self):
        front = self.front_entry.get().strip()
        back = self.back_entry.get().strip()
 
        if not front or not back:
            self.form_error_label.configure(text="Both front and back are required.")
            return
 
        card = Card(deck_id=self.deck_id, front_text=front, back_text=back)
        self.master_app.session.add(card)
        self.master_app.session.commit()
 
        self.front_entry.delete(0, "end")
        self.back_entry.delete(0, "end")
        self.form_error_label.configure(text="")
 
        self._refresh_card_list()
        self.refresh_header_review_button()

    def refresh_header_review_button(self):
        for widget in self.winfo_children():
            widget.destroy()
        self._build_header()
        self._build_add_card_form()
        self._build_card_list()
 