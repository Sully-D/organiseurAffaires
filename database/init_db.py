from .db import engine, Base, SessionLocal
from .models import KanbanColumn

def init_db():
    Base.metadata.create_all(bind=engine)
    
    # Initialize default columns if not present
    session = SessionLocal()
    
    desired_columns = [
        "À faire", "En attente", "En cours", "Traitements", 
        "Tâches", "CTA", "Réparations", "Terminé", "Important"
    ]
    
    # Get existing columns map
    existing_cols = session.query(KanbanColumn).all()
    existing_map = {c.name: c for c in existing_cols}
    
    for i, name in enumerate(desired_columns):
        if name in existing_map:
            # Update order if changed
            if existing_map[name].order_index != i:
                 existing_map[name].order_index = i
        else:
            # Create new column
            col = KanbanColumn(name=name, order_index=i)
            session.add(col)
            
    session.commit()
    session.close()

if __name__ == "__main__":
    init_db()
