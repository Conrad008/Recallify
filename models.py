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