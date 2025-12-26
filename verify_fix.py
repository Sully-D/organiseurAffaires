from database.db import SessionLocal
from database.models import Activity, KanbanColumn, Scelle
from datetime import date

def test_db_ops():
    db = SessionLocal()
    
    # 1. Test creation
    cols = db.query(KanbanColumn).all()
    first_col = cols[0]
    
    act = Activity()
    act.column_id = first_col.id
    # Simulate the fixed logic: set attrs then flush
    act.name = "Test Activity"
    act.date = date.today()
    act.description = "Test Desc"
    
    db.add(act)
    db.flush()
    print(f"Created Activity ID: {act.id}")
    
    # 2. Test Scelle addition
    sc = Scelle(name="Scelle 1", info="Info", activity_id=act.id)
    db.add(sc)
    db.commit()
    print("Committed Activity and Scelle")
    
    # 3. Test Scelle modification
    sc_check = db.query(Scelle).filter(Scelle.name=="Scelle 1").first()
    if sc_check:
        sc_check.name = "Scelle 1 Modified"
        db.commit()
        print("Modified Scelle")
    
    # 4. Verify
    final_chk = db.query(Activity).filter(Activity.id == act.id).first()
    print(f"Activity Name: {final_chk.name}, Scelle Name: {final_chk.scelles[0].name}")
    
    db.close()

if __name__ == "__main__":
    test_db_ops()
