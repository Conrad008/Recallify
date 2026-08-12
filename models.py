from datetime import datetime, date
 
from sqlalchemy import (
    Column, Integer, String, Float, Date, DateTime, ForeignKey
)
from sqlalchemy.orm import relationship
 
from database import Base

class User(Base):
    __tablename__ = "users"
 
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
 
    decks = relationship("Deck", back_populates="owner", cascade="all, delete-orphan")
 
    def __repr__(self):
        return f"<User id={self.id} username={self.username!r}>"

class Deck(Base):
    __tablename__ = "decks"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="decks")
    cards = relationship("Card", back_populates="deck", cascade="all, delete-orphan")

    def due_cards(self, session, today: date = None):
        today = today or date.today()
        return [c for c in self.cards if c.next_review_date <= today]

    def __repr__(self):
        return f"<Deck id={self.id} name={self.name!r}>"

class Card(Base):
    __tablename__ = "cards"
 
    id = Column(Integer, primary_key=True)
    deck_id = Column(Integer, ForeignKey("decks.id"), nullable=False)
 
    front_text = Column(String, nullable=False)
    back_text = Column(String, nullable=False)
 

    image_path = Column(String, nullable=True)
 
    easiness_factor = Column(Float, default=2.5)
    repetitions = Column(Integer, default=0)
    interval = Column(Integer, default=0)  
    next_review_date = Column(Date, default=date.today)
 
    created_at = Column(DateTime, default=datetime.utcnow)
 
    deck = relationship("Deck", back_populates="cards")
    review_logs = relationship("ReviewLog", back_populates="card", cascade="all, delete-orphan")
 
    @property
    def status(self) -> str:

        if self.repetitions == 0:
            return "new"
        if self.interval >= 21:
            return "mastered"
        return "learning"
 
    def __repr__(self):
        return f"<Card id={self.id} front={self.front_text[:20]!r}>"

class ReviewLog(Base):
    __tablename__ = "review_logs"
 
    id = Column(Integer, primary_key=True)
    card_id = Column(Integer, ForeignKey("cards.id"), nullable=False)
 
    reviewed_at = Column(DateTime, default=datetime.utcnow)
    quality_rating = Column(Integer, nullable=False)  
    interval_before = Column(Integer)
    interval_after = Column(Integer)
    easiness_before = Column(Float)
    easiness_after = Column(Float)
 
    card = relationship("Card", back_populates="review_logs")
 
    def __repr__(self):
        return f"<ReviewLog card_id={self.card_id} quality={self.quality_rating}>"