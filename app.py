import customtkinter as ctk
 
from database import init_db, get_session

from ui.login_view import LoginView
from ui.deck_list_view import DeckListView
 
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