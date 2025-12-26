from PySide6.QtWidgets import (
    QMainWindow, QToolBar, QWidget, QVBoxLayout, QFileDialog, QMessageBox, QLineEdit,
    QComboBox, QLabel, QHBoxLayout
)
from PySide6.QtGui import QAction
from .kanban import KanbanBoard
from .forms import ActivityDialog, ColumnManagerDialog
from .styles import DARK_THEME
from database.models import Tag

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Organiseur d'Affaires")
        self.resize(1000, 700)
        self.setStyleSheet(DARK_THEME)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout(self.central_widget)
        
        # Toolbar
        self.toolbar = QToolBar("Outils")
        self.addToolBar(self.toolbar)
        
        new_act_action = QAction("Nouvelle Activité", self)
        new_act_action.triggered.connect(self.new_activity)
        self.toolbar.addAction(new_act_action)
        
        col_mgr_action = QAction("Gérer Colonnes", self)
        col_mgr_action.triggered.connect(self.manage_columns)
        self.toolbar.addAction(col_mgr_action)

        export_action = QAction("Exporter PDF", self)
        export_action.triggered.connect(self.export_action)
        self.toolbar.addAction(export_action)
        
        export_daily_action = QAction("Exporter Journalier HTML", self)
        export_daily_action.triggered.connect(self.export_daily_action)
        self.toolbar.addAction(export_daily_action)
        
        refresh_action = QAction("Rafraîchir", self)
        refresh_action.triggered.connect(self.refresh_view)
        self.toolbar.addAction(refresh_action)

        # Search Bar & Sort
        search_layout = QHBoxLayout()
        self.search_bar = QComboBox()
        self.search_bar.setEditable(True)
        self.search_bar.setInsertPolicy(QComboBox.NoInsert)
        self.search_bar.lineEdit().setPlaceholderText("Rechercher (Taper ou Sélectionner Tags)...")
        # Ensure ClearButton on lineEdit inside combo?
        self.search_bar.lineEdit().setClearButtonEnabled(True)
        self.search_bar.editTextChanged.connect(self.refresh_view)
        
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["Date (Croissant)", "Date (Décroissant)", "Nom (A-Z)", "Nom (Z-A)"])
        self.sort_combo.currentIndexChanged.connect(self.refresh_view)
        
        search_layout.addWidget(self.search_bar)
        search_layout.addWidget(QLabel("Trier par:"))
        search_layout.addWidget(self.sort_combo)
        
        self.layout.addLayout(search_layout)
        
        # Kanban
        # In a real app we might want to keep reference to the board to call its methods
        self.kanban_board = KanbanBoard(self)
        self.layout.addWidget(self.kanban_board)
        
        # Populate Search Tags
        self.load_search_tags()

    def load_search_tags(self):
        # Fetch all tags
        try:
            tags = self.kanban_board.db.query(Tag).all()
            tag_names = sorted(list(set([t.name for t in tags]))) # Unique and sorted
            self.search_bar.clear()
            self.search_bar.addItems(tag_names)
            self.search_bar.setCurrentIndex(-1) # No selection initially
        except Exception:
            pass # DB might not be ready or empty

    def new_activity(self):
        self.open_activity_dialog()

    def manage_columns(self):
        dialog = ColumnManagerDialog(self)
        dialog.exec()
        self.refresh_view()

    def open_activity_dialog(self, activity_id=None):
        dialog = ActivityDialog(activity_id, self)
        if dialog.exec():
            self.refresh_view()

    def refresh_view(self):
        sort_text = self.sort_combo.currentText()
        sort_by = "date"
        sort_order = "asc"
        
        if "Nom" in sort_text:
            sort_by = "name"
        
        if "Décroissant" in sort_text or "Z-A" in sort_text:
            sort_order = "desc"
            
        if "Décroissant" in sort_text or "Z-A" in sort_text:
            sort_order = "desc"
            
        search_text = self.search_bar.currentText()
        self.kanban_board.refresh(sort_by, sort_order, search_text)
        
        # Reload tags to ensure we have the latest list
        self.search_bar.blockSignals(True)
        self.load_search_tags()
        self.search_bar.setEditText(search_text) # Restore text
        self.search_bar.blockSignals(False)

    def export_action(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Exporter en PDF", "", "PDF Files (*.pdf)")
        if filename:
            try:
                # Add .pdf extension if missing (though Qt usually handles this)
                if not filename.lower().endswith(".pdf"):
                    filename += ".pdf"
                    
                from export import export_to_pdf
                # Pass self.kanban_board to capture the snapshot
                export_to_pdf(filename, self.kanban_board)
                QMessageBox.information(self, "Succès", "Export PDF réussi !")
            except Exception as e:
                import traceback
                traceback.print_exc()
                QMessageBox.critical(self, "Erreur", f"Erreur lors de l'export: {str(e)}")

    def export_daily_action(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Exporter Journalier HTML", "", "HTML Files (*.html)")
        if filename:
            try:
                if not filename.lower().endswith(".html"):
                    filename += ".html"
                
                from export import export_daily_to_html
                export_daily_to_html(filename)
                QMessageBox.information(self, "Succès", "Export Journalier HTML réussi !")
            except Exception as e:
                import traceback
                traceback.print_exc()
                QMessageBox.critical(self, "Erreur", f"Erreur lors de l'export HTML: {str(e)}")
