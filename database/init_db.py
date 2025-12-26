from .db import engine, Base, SessionLocal
from .models import KanbanColumn

def init_db():
    Base.metadata.create_all(bind=engine)
    
    # Initialize default columns if not present
    session = SessionLocal()
    if session.query(KanbanColumn).count() == 0:
        default_columns = ["À faire", "En cours", "Terminé"]
        for i, name in enumerate(default_columns):
            col = KanbanColumn(name=name, order_index=i)
            session.add(col)
        session.commit()
    session.close()

if __name__ == "__main__":
    init_db()
