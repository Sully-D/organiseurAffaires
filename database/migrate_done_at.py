from database.db import engine, Base
from sqlalchemy import text

def migrate():
    with engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE taches ADD COLUMN done_at DATE"))
            print("Added column done_at to taches")
        except Exception as e:
            print(f"Error adding done_at to taches (might already exist): {e}")

        try:
            conn.execute(text("ALTER TABLE traitements ADD COLUMN done_at DATE"))
            print("Added column done_at to traitements")
        except Exception as e:
            print(f"Error adding done_at to traitements (might already exist): {e}")

if __name__ == "__main__":
    migrate()
