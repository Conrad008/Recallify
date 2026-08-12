import customtkinter as ctk
 
from database import init_db, get_session

from login import LoginView
from deck import DeckListView
 
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
 
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
 
        self.title("SpacedCards")
        self.geometry("900x650")
        self.minsize(700, 500)

        init_db()
        self.session = get_session()

        self.current_user = None
 
        self.current_frame = None
        self.show_login()

def show_login(self):
    self._switch(LoginView(self, on_login_success=self.on_login_success))
 
def on_login_success(self, user):
    self.current_user = user
    self.show_deck_list()
 
def show_deck_list(self):
    self._switch(DeckListView(self))
 
def show_deck_detail(self, deck_id: int):
    from deck import DeckDetailView
    self._switch(DeckDetailView(self, deck_id))
 
def show_review(self, deck_id: int):
    from ui.review_view import ReviewView
    self._switch(ReviewView(self, deck_id))
 
def show_stats(self, deck_id: int = None):
    from ui.stats_view import StatsView
    self._switch(StatsView(self, deck_id))
 
def logout(self):
    self.current_user = None
    self.show_login()
 
def _switch(self, frame: ctk.CTkFrame):
    if self.current_frame is not None:
        self.current_frame.destroy()
    self.current_frame = frame
    self.current_frame.pack(fill="both", expand=True)
 
def on_closing(self):
    self.session.close()
    self.destroy()

def run():
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
 