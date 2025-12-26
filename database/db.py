from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Utilisation de SQLite par défaut
DATABASE_URL = "sqlite:///organiseur.db"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
