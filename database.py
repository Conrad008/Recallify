from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
 
DATABASE_URL = "sqlite:///flashcards.db"
 
engine = create_engine(DATABASE_URL, echo=False)
 
Base = declarative_base()
 
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def init_db():

    import models  
    Base.metadata.create_all(bind=engine)

def get_session():

    return SessionLocal()