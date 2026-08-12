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
            header, text="+ New Deck", width=120, command=self.open_new_deck_dialog
        )
        new_deck_btn.pack(side="right", padx=(0, 10))

    def build_deck_list(self):
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True, padx=24, pady=10)
 
        self.refresh_decks()
 
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
            self.build_deck_card(deck)

    def build_deck_card(self, deck: Deck):
        due_count = len(deck.due_cards(self.master_app.session))
        card_count = len(deck.cards)
 
        card = ctk.CTkFrame(self.scroll_frame, corner_radius=10)
        card.pack(fill="x", pady=6)
 
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, padx=16, pady=12)
 
        name_label = ctk.CTkLabel(
            info_frame, text=deck.name, font=ctk.CTkFont(size=16, weight="bold"), anchor="w"
        )
        name_label.pack(anchor="w")
 
        detail_text = f"{card_count} card{'s' if card_count != 1 else ''}"
        if due_count:
            detail_text += f"  •  {due_count} due today"
        detail_label = ctk.CTkLabel(
            info_frame, text=detail_text, text_color="gray", anchor="w"
        )
        detail_label.pack(anchor="w")
 
        button_frame = ctk.CTkFrame(card, fg_color="transparent")
        button_frame.pack(side="right", padx=16, pady=12)
 
        open_btn = ctk.CTkButton(
            button_frame, text="Open", width=80,
            command=lambda d=deck: self.master_app.show_deck_detail(d.id),
        )
        open_btn.pack(side="left", padx=4)
 
        review_btn = ctk.CTkButton(
            button_frame, text=f"Review ({due_count})", width=110,
            state="normal" if due_count else "disabled",
            fg_color="#2fa572" if due_count else "gray",
            command=lambda d=deck: self.master_app.show_review(d.id),
        )
        review_btn.pack(side="left", padx=4)
     
    def open_new_deck_dialog(self):
        dialog = ctk.CTkInputDialog(text="Deck name:", title="New Deck")
        name = dialog.get_input()
 
        if name and name.strip():
            deck = Deck(user_id=self.master_app.current_user.id, name=name.strip())
            self.master_app.session.add(deck)
            self.master_app.session.commit()
            self.refresh_decks()