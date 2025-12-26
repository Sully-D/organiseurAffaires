from database.db import SessionLocal
from database.models import KanbanColumn

def test_cols():
    db = SessionLocal()
    
    # 1. Add Column
    new_col = KanbanColumn(name="Colonne Test", order_index=99)
    db.add(new_col)
    db.commit()
    print(f"Added column: {new_col.name}")
    
    # 2. Check
    exists = db.query(KanbanColumn).filter(KanbanColumn.name=="Colonne Test").first()
    assert exists is not None
    
    # 3. Delete
    db.delete(exists)
    db.commit()
    print("Deleted column")
    
    db.close()

if __name__ == "__main__":
    test_cols()
