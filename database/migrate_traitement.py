from database.db import engine
from sqlalchemy import text

def migrate():
    with engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE traitements ADD COLUMN done BOOLEAN DEFAULT 0"))
            print("Added done to traitements")
        except Exception as e:
            print(f"Migration error (might already exist): {e}")

if __name__ == "__main__":
    migrate()
