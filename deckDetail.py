import customtkinter as ctk
 
from models import Card, Deck
from csvImporter import CSVImporter
from tkinter import filedialog

 
 
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
 
        self.refresh_card_list()
        self.refresh_header_review_button()

    def on_import_csv(self):
        file_path = filedialog.askopenfilename(
            title="Select a CSV file",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        )
        if not file_path:
            return  # user cancelled the dialog
 
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            self.form_error_label.configure(text=f"Could not read file: {e}")
            return
 
        cards = CSVImporter.import_cards(content, self.deck_id)
 
        if not cards:
            self.form_error_label.configure(
                text="No valid rows found. Expected columns: front, back"
            )
            return
 
        self.master_app.session.add_all(cards)
        self.master_app.session.commit()
 
        self.form_error_label.configure(text=f"Imported {len(cards)} card(s).", text_color="#2fa572")
        self.refresh_header_review_button()

    def refresh_header_review_button(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.build_header()
        self.build_add_card_form()
        self.build_card_list()
     
    def build_card_list(self):
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True, padx=24, pady=(0, 20))
        self.refresh_card_list()
 
    def refresh_card_list(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
 
        self.master_app.session.refresh(self.deck)
        cards = self.deck.cards
 
        if not cards:
            empty_label = ctk.CTkLabel(
                self.scroll_frame, text="No cards yet. Add one above.", text_color="gray"
            )
            empty_label.pack(pady=30)
            return
 
        for card in cards:
            row = ctk.CTkFrame(self.scroll_frame, corner_radius=8)
            row.pack(fill="x", pady=4)
 
            front_label = ctk.CTkLabel(
                row, text=card.front_text, anchor="w", font=ctk.CTkFont(weight="bold")
            )
            front_label.pack(side="left", padx=(12, 8), pady=8)
 
            back_label = ctk.CTkLabel(row, text=f"→ {card.back_text}", anchor="w", text_color="gray")
            back_label.pack(side="left", padx=(0, 8), pady=8)
 
            status_label = ctk.CTkLabel(row, text=card.status, text_color="#2fa572")
            status_label.pack(side="right", padx=12)
 