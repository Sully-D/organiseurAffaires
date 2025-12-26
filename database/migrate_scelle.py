from database.db import engine
from sqlalchemy import text

def migrate():
    with engine.connect() as conn:
        try:
            # Check if columns exist is hard in pure sqlite/sa without inspection, 
            # but for simple add column we can try catch
            
            # cta_validated
            try:
                conn.execute(text("ALTER TABLE scelles ADD COLUMN cta_validated BOOLEAN DEFAULT 0"))
                print("Added cta_validated")
            except Exception as e:
                print(f"Skipped cta_validated: {e}")

            # reparations_validated
            try:
                conn.execute(text("ALTER TABLE scelles ADD COLUMN reparations_validated BOOLEAN DEFAULT 0"))
                print("Added reparations_validated")
            except Exception as e:
                 print(f"Skipped reparations_validated: {e}")
                 
            # reparations_details
            try:
                conn.execute(text("ALTER TABLE scelles ADD COLUMN reparations_details TEXT"))
                print("Added reparations_details")
            except Exception as e:
                 print(f"Skipped reparations_details: {e}")
            
            # important_info
            try:
                conn.execute(text("ALTER TABLE scelles ADD COLUMN important_info TEXT"))
                print("Added important_info")
            except Exception as e:
                 print(f"Skipped important_info: {e}")
                 
        except Exception as e:
            print(f"Migration error: {e}")

if __name__ == "__main__":
    migrate()
