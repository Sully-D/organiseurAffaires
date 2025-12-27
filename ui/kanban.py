from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QLabel, QFrame, 
    QMenu, QMessageBox
)
from PySide6.QtCore import Qt, QMimeData, QPoint
from PySide6.QtGui import QDrag, QCursor
from sqlalchemy import or_, and_, cast, String
from database.db import SessionLocal
from datetime import date
from database.models import KanbanColumn, Activity, Tag, Scelle, Traitement, Tache

class ActivityCard(QFrame):
    def __init__(self, activity, parent=None):
        super().__init__(parent)
        self.course_id = activity.id
        self.setObjectName("ActivityCard")
        
        # Check Overdue Status
        today = date.today()
        
        # Check actual physical column of the activity
        real_column_name = ""
        if activity.column:
            real_column_name = activity.column.name.upper()
            
        # Is overdue if date < today AND not physically in "Terminé"
        is_terminated = "TERMINÉ" in real_column_name or "TERMINE" in real_column_name
        
        if activity.date and activity.date < today and not is_terminated:
            self.setProperty("overdue", True)
        else:
             self.setProperty("overdue", False)
        
        layout = QVBoxLayout(self)
        title = QLabel(activity.name)
        title.setObjectName("CardTitle")
        layout.addWidget(title)
        
        date_lbl = QLabel(f"Date: {activity.date}")
        layout.addWidget(date_lbl)
        
        # Scelles Detail
        if activity.scelles:
            layout.addWidget(QLabel("--- Scellés ---"))
            for sc in activity.scelles:
                # Scelle Container
                sc_frame = QFrame()
                sc_frame.setProperty("class", "ScelleFrame")
                sc_layout = QVBoxLayout(sc_frame)
                sc_layout.setContentsMargins(4, 4, 4, 4)
                
                # Header: Name + Name Badge
                name_lbl = QLabel(f"📦 {sc.name}")
                name_lbl.setProperty("class", "ScelleName") 
                sc_layout.addWidget(name_lbl)
                
                # Badges Row
                badges_layout = QHBoxLayout()
                badges_layout.setSpacing(2)
                badges_layout.setAlignment(Qt.AlignLeft)
                
                if sc.cta_validated:
                    lbl = QLabel("CTA OK")
                    lbl.setProperty("class", "BadgeCTA")
                    badges_layout.addWidget(lbl)
                    
                if sc.reparations_validated:
                    lbl = QLabel("RÉPARATIONS")
                    lbl.setProperty("class", "BadgeRep")
                    badges_layout.addWidget(lbl)
                
                if badges_layout.count() > 0:
                    sc_layout.addLayout(badges_layout)
                
                # IMPORTANT Info
                if sc.important_info:
                    imp_lbl = QLabel(f"⚠ {sc.important_info}")
                    imp_lbl.setProperty("class", "BadgeImportant")
                    imp_lbl.setWordWrap(True)
                    sc_layout.addWidget(imp_lbl)
                
                # Counts
                # Counts (Ignore if CTA or Reparations validated)
                is_scelle_validated = sc.cta_validated or sc.reparations_validated
                
                t_count = 0
                tr_count = 0
                
                if not is_scelle_validated:
                    t_count = len([t for t in sc.taches if not t.done])
                    tr_count = len([tr for tr in sc.traitements if not tr.done])
                if t_count > 0 or tr_count > 0:
                    counts = []
                    if t_count: counts.append(f"{t_count} Tâches")
                    if tr_count: counts.append(f"{tr_count} Traitements")
                    count_lbl = QLabel(", ".join(counts))
                    count_lbl.setStyleSheet("color: #aaa; font-size: 11px;")
                    sc_layout.addWidget(count_lbl)
                
                layout.addWidget(sc_frame)
        else:
            layout.addWidget(QLabel("<i>Aucun scellé</i>"))
        
        # Tags styling could be added here
        
    def mouseMoveEvent(self, e):
        if e.buttons() == Qt.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            mime.setText(str(self.course_id))
            drag.setMimeData(mime)
            drag.exec(Qt.MoveAction)

class KanbanColumnWidget(QFrame):
    def __init__(self, column_model, parent_board):
        super().__init__()
        self.column_id = column_model.id
        self.column_name = column_model.name # Store for child access
        self.parent_board = parent_board
        self.setObjectName("KanbanColumn")
        self.setAcceptDrops(True)
        self.setMinimumWidth(250)
        
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)
        
        title = QLabel(column_model.name)
        title.setObjectName("ColumnTitle")
        self.layout.addWidget(title)
        
        self.cards_layout = QVBoxLayout()
        self.layout.addLayout(self.cards_layout)
        
    def add_card(self, activity):
        card = ActivityCard(activity, self)
        # Handle double click to edit
        card.mouseDoubleClickEvent = lambda e: self.parent_board.edit_activity(activity.id)
        self.cards_layout.addWidget(card)
        
    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        activity_id = int(e.mimeData().text())
        self.parent_board.move_activity(activity_id, self.column_id)
        e.accept()

class KanbanBoard(QScrollArea):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWidgetResizable(True)
        
        self.content_widget = QWidget()
        self.h_layout = QHBoxLayout(self.content_widget)
        self.h_layout.setAlignment(Qt.AlignLeft)
        self.setWidget(self.content_widget)
        
        self.db = SessionLocal()
        self.refresh()
        
    def refresh(self, sort_by="date", sort_order="asc", search_text=""):
        self.db.expire_all() # Ensure we see latest changes from other sessions (like ActivityDialog)
        
        # Clear existing
        for i in reversed(range(self.h_layout.count())): 
            self.h_layout.itemAt(i).widget().setParent(None)
            
        # Get "En attente" column ID for filtering
        en_attente_col = self.db.query(KanbanColumn).filter(KanbanColumn.name == "En attente").first()
        en_attente_id = en_attente_col.id if en_attente_col else -1
        
        columns = self.db.query(KanbanColumn).order_by(KanbanColumn.order_index).all()

        for col in columns:
            col_widget = KanbanColumnWidget(col, self)
            
            # Virtual Columns Logic
            if col.name == "Traitements":
                # Activities with pending treatments (EXCLUDING those in Validated Scelles OR in En attente)
                query = self.db.query(Activity).join(Activity.scelles).join(Scelle.traitements).filter(
                    Traitement.done == False,
                    Scelle.cta_validated == False,
                    Scelle.reparations_validated == False
                ).filter(Activity.column_id != en_attente_id).distinct()
            
            elif col.name == "Tâches":
                # Activities with pending tasks (EXCLUDING those in Validated Scelles OR in En attente)
                query = self.db.query(Activity).join(Activity.scelles).join(Scelle.taches).filter(
                    Tache.done == False,
                    Scelle.cta_validated == False,
                    Scelle.reparations_validated == False
                ).filter(Activity.column_id != en_attente_id).distinct()
            
            elif col.name and col.name.upper() == "CTA":
                 # Activities with CTA Validated
                 query = self.db.query(Activity).join(Activity.scelles).filter(Scelle.cta_validated == True).distinct()
                 
            elif col.name and col.name.upper().startswith("RÉPARATION"): # Handle "Réparations", "Réparation", "Reparations"
                 # Activities with Reparations Validated (checked)
                 query = self.db.query(Activity).join(Activity.scelles).filter(Scelle.reparations_validated == True).distinct()

            elif col.name and col.name.upper() in ["IMPORTANT", "IMPORTANTS"]:
                 # Activities with Important info
                 query = self.db.query(Activity).join(Activity.scelles).filter(or_(Scelle.important_info != None, Scelle.important_info != "")).filter(Scelle.important_info != "").distinct()

            elif col.name and col.name.upper() == "EN COURS":
                # User request: "En cours" should also show pending treatments/tasks FROM OTHER COLUMNS.
                # BUT ignore if Scelle is validated (CTA or Rep) AND ignore if in En attente
                query = self.db.query(Activity).outerjoin(Activity.scelles).outerjoin(Scelle.traitements).outerjoin(Scelle.taches).filter(
                    or_(
                        Activity.column_id == col.id,
                        and_(Traitement.done == False, Scelle.cta_validated == False, Scelle.reparations_validated == False)
                    )
                ).filter(
                     or_(
                        Activity.column_id == col.id, # Always include if physically here
                        Activity.column_id != en_attente_id # Otherwise must NOT be in En attente
                     )
                ).distinct()
                # Correction: The logic above for "En cours" is slightly complex with ORs.
                # Simplest way:
                # 1. Base Criteria for "pending stuff" OR "is here"
                # 2. Filter: If it is NOT here, it MUST NOT be in En attente.
                # Equivalently: .filter(or_(Activity.column_id == col.id, Activity.column_id != en_attente_id))
                # Wait, if col.id != en_attente_id (which is true), then `Activity.column_id == col.id` implies `Activity.column_id != en_attente_id`.
                # So `Activity.column_id != en_attente_id` covers both cases!
                # If it's in En cours, it's not in En attente.
                # If it's in another column (e.g. To Do), it's not in En attente.
                # If it IS in En attente, we exclude it.
                # So just .filter(Activity.column_id != en_attente_id) works perfectly.
                
                query = self.db.query(Activity).outerjoin(Activity.scelles).outerjoin(Scelle.traitements).outerjoin(Scelle.taches).filter(
                    or_(
                        Activity.column_id == col.id,
                        and_(Traitement.done == False, Scelle.cta_validated == False, Scelle.reparations_validated == False),
                        and_(Tache.done == False, Scelle.cta_validated == False, Scelle.reparations_validated == False)
                    )
                ).filter(Activity.column_id != en_attente_id).distinct()

            else:
                # Standard Column
                query = self.db.query(Activity).filter(Activity.column_id == col.id)
            
            # Apply Common Filters (Search & Sort)
            if search_text:
                search_term = f"%{search_text}%"
                query = query.filter(
                    or_(
                        Activity.name.ilike(search_term),
                        Activity.description.ilike(search_term),
                        cast(Activity.date, String).ilike(search_term),
                        Activity.tags.any(Tag.name.ilike(search_term)),
                        Activity.scelles.any(Scelle.name.ilike(search_term)),
                        Activity.scelles.any(Scelle.info.ilike(search_term)),
                        Activity.scelles.any(Scelle.important_info.ilike(search_term)),
                        Activity.scelles.any(Scelle.reparations_details.ilike(search_term)),
                        Activity.scelles.any(Scelle.traitements.any(Traitement.description.ilike(search_term))),
                        Activity.scelles.any(Scelle.taches.any(Tache.description.ilike(search_term)))
                    )
                )

            if sort_by == "date":
                query = query.order_by(Activity.date.asc() if sort_order == "asc" else Activity.date.desc())
            elif sort_by == "name":
                query = query.order_by(Activity.name.asc() if sort_order == "asc" else Activity.name.desc())
            
            activities = query.all()
            for act in activities:
                col_widget.add_card(act)
            self.h_layout.addWidget(col_widget)
            
    def move_activity(self, activity_id, new_column_id):
        activity = self.db.query(Activity).filter(Activity.id == activity_id).first()
        if activity:
            activity.column_id = new_column_id
            self.db.commit()
            self.refresh()

    def edit_activity(self, activity_id):
        self.main_window.open_activity_dialog(activity_id)

    def closeEvent(self, event):
        self.db.close()
        super().closeEvent(event)
