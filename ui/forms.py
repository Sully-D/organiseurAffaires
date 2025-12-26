from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, 
    QTextEdit, QDateEdit, QPushButton, QWidget, QLabel, QScrollArea, QListWidget, QListWidgetItem,
    QInputDialog, QMessageBox, QTabWidget, QCheckBox, QGroupBox
)
from PySide6.QtCore import QDate, Qt
from database.db import SessionLocal
from database.models import Activity, Scelle, KanbanColumn, Tag, Tache, Traitement

class ColumnManagerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gérer les Colonnes")
        self.setMinimumWidth(400)
        self.setMinimumHeight(300)
        
        self.db = SessionLocal()
        
        self.layout = QVBoxLayout(self)
        
        self.col_list = QListWidget()
        self.layout.addWidget(self.col_list)
        
        btn_layout = QHBoxLayout()
        add_btn = QPushButton("Ajouter")
        add_btn.clicked.connect(self.add_column)
        del_btn = QPushButton("Supprimer")
        del_btn.clicked.connect(self.delete_column)
        
        up_btn = QPushButton("Monter")
        up_btn.clicked.connect(self.move_up)
        down_btn = QPushButton("Descendre")
        down_btn.clicked.connect(self.move_down)
        
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(del_btn)
        btn_layout.addWidget(up_btn)
        btn_layout.addWidget(down_btn)
        self.layout.addLayout(btn_layout)
        
        self.load_columns()
        
    def load_columns(self):
        self.col_list.clear()
        columns = self.db.query(KanbanColumn).order_by(KanbanColumn.order_index).all()
        for col in columns:
            item = QListWidgetItem(f"{col.name}")
            item.setData(Qt.UserRole, col.id)
            self.col_list.addItem(item)
            
    def add_column(self):
        name, ok = QInputDialog.getText(self, "Nouvelle Colonne", "Nom de la colonne:")
        if ok and name:
            # Check exist
            exists = self.db.query(KanbanColumn).filter(KanbanColumn.name == name).first()
            if exists:
                QMessageBox.warning(self, "Erreur", "Cette colonne existe déjà")
                return
                
            # Get max index
            max_idx = 0
            cols = self.db.query(KanbanColumn).all()
            if cols:
                max_idx = max(c.order_index for c in cols) + 1
            
            new_col = KanbanColumn(name=name, order_index=max_idx)
            self.db.add(new_col)
            self.db.commit()
            self.load_columns()

    def delete_column(self):
        row = self.col_list.currentRow()
        if row < 0:
            return
            
        item = self.col_list.item(row)
        col_id = item.data(Qt.UserRole)
        
        col = self.db.query(KanbanColumn).filter(KanbanColumn.id == col_id).first()
        if not col:
            return
            
        # Check if empty
        if col.activities:
            QMessageBox.warning(self, "Impossible", "La colonne n'est pas vide. Déplacez d'abord les activités.")
            return
            
        self.db.delete(col)
        self.db.commit()
        self.load_columns()

    def swap_order(self, col1, col2):
        col1.order_index, col2.order_index = col2.order_index, col1.order_index
        self.db.commit()
        self.load_columns()

    def move_up(self):
        row = self.col_list.currentRow()
        if row <= 0: return # First item or none selected
        
        curr_id = self.col_list.item(row).data(Qt.UserRole)
        prev_id = self.col_list.item(row-1).data(Qt.UserRole)
        
        curr_col = self.db.query(KanbanColumn).get(curr_id)
        prev_col = self.db.query(KanbanColumn).get(prev_id)
        
        self.swap_order(curr_col, prev_col)
        self.col_list.setCurrentRow(row-1)

    def move_down(self):
        row = self.col_list.currentRow()
        if row < 0 or row >= self.col_list.count() - 1: return
        
        curr_id = self.col_list.item(row).data(Qt.UserRole)
        next_id = self.col_list.item(row+1).data(Qt.UserRole)
        
        curr_col = self.db.query(KanbanColumn).get(curr_id)
        next_col = self.db.query(KanbanColumn).get(next_id)
        
        self.swap_order(curr_col, next_col)
        self.col_list.setCurrentRow(row+1)

    def closeEvent(self, event):
        self.db.close()
        super().closeEvent(event)

class ScelleDialog(QDialog):
    def __init__(self, scelle_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Détail Scellé")
        self.setMinimumWidth(500)
        self.setMinimumHeight(600)
        
        # scelle_data can be Scelle object or dict
        self.data = scelle_data
        self.is_obj = hasattr(self.data, 'id')
        
        self.layout = QVBoxLayout(self)
        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)
        
        # --- Tab 1: Général & Validation ---
        self.tab_general = QWidget()
        self.gen_layout = QVBoxLayout(self.tab_general)
        
        form = QFormLayout()
        self.name_edit = QLineEdit()
        self.name_edit.setText(self.data.name if self.is_obj else self.data['name'])
        
        self.info_edit = QTextEdit()
        self.info_edit.setMaximumHeight(60)
        self.info_edit.setText((self.data.info if self.is_obj else self.data.get('info', '')) or "")
        
        self.important_edit = QTextEdit()
        self.important_edit.setMaximumHeight(60)
        self.important_edit.setStyleSheet("border: 1px solid red;")
        val = self.data.important_info if self.is_obj else self.data.get('important_info', '')
        self.important_edit.setText(val or "")
        
        form.addRow("Nom:", self.name_edit)
        form.addRow("Infos:", self.info_edit)
        form.addRow("IMPORTANT:", self.important_edit)
        self.gen_layout.addLayout(form)
        
        # CTA & Réparations
        self.grp_valid = QGroupBox("Validations")
        v_layout = QVBoxLayout(self.grp_valid)
        
        self.chk_cta = QCheckBox("CTA Validé")
        self.chk_cta.setChecked(self.data.cta_validated if self.is_obj else self.data.get('cta_validated', False))
        
        self.chk_rep = QCheckBox("Réparations à faire")
        self.chk_rep.setChecked(self.data.reparations_validated if self.is_obj else self.data.get('reparations_validated', False))
        self.chk_rep.toggled.connect(self.toggle_rep_details)
        
        self.rep_details = QTextEdit()
        self.rep_details.setPlaceholderText("Détail des réparations...")
        self.rep_details.setVisible(self.chk_rep.isChecked())
        val_rep = self.data.reparations_details if self.is_obj else self.data.get('reparations_details', '')
        self.rep_details.setText(val_rep or "")
        
        v_layout.addWidget(self.chk_cta)
        v_layout.addWidget(self.chk_rep)
        v_layout.addWidget(self.rep_details)
        self.gen_layout.addWidget(self.grp_valid)
        
        self.tabs.addTab(self.tab_general, "Général")

        # --- Tab 2: Traitements ---
        self.tab_trait = QWidget()
        t_layout = QVBoxLayout(self.tab_trait)
        self.trait_list = QListWidget()
        t_layout.addWidget(self.trait_list)
        
        tb_layout = QHBoxLayout()
        add_t_btn = QPushButton("+ Traitement")
        add_t_btn.clicked.connect(self.add_traitement)
        del_t_btn = QPushButton("- Supprimer")
        del_t_btn.clicked.connect(self.del_traitement)
        tb_layout.addWidget(add_t_btn)
        tb_layout.addWidget(del_t_btn)
        t_layout.addLayout(tb_layout)
        
        self.load_traitements()
        self.tabs.addTab(self.tab_trait, "Traitements")
        
        # --- Tab 3: Tâches ---
        self.tab_task = QWidget()
        tk_layout = QVBoxLayout(self.tab_task)
        self.task_list = QListWidget()
        tk_layout.addWidget(self.task_list)
        
        tkb_layout = QHBoxLayout()
        add_tk_btn = QPushButton("+ Tâche")
        add_tk_btn.clicked.connect(self.add_task)
        del_tk_btn = QPushButton("- Supprimer")
        del_tk_btn.clicked.connect(self.del_task)
        tkb_layout.addWidget(add_tk_btn)
        tkb_layout.addWidget(del_tk_btn)
        tk_layout.addLayout(tkb_layout)
        
        self.load_tasks()
        self.tabs.addTab(self.tab_task, "Tâches")
        
        # Save Buttons
        btn_box = QHBoxLayout()
        save = QPushButton("Valider Scellé")
        save.clicked.connect(self.save)
        cancel = QPushButton("Annuler")
        cancel.clicked.connect(self.reject)
        btn_box.addWidget(save)
        btn_box.addWidget(cancel)
        self.layout.addLayout(btn_box)

    def toggle_rep_details(self, checked):
        self.rep_details.setVisible(checked)

    def load_traitements(self):
        self.trait_list.clear()
        if self.is_obj:
            if hasattr(self.data, '_temp_traitements'):
                items = self.data._temp_traitements
                for t in items:
                    # _temp items are dicts
                    self.add_list_item(self.trait_list, t['description'], t, t['done'])
            else:
                items = self.data.traitements
                for t in items:
                    self.add_list_item(self.trait_list, t.description, t, t.done)
        else:
            items = self.data.get('traitements', [])
            for t in items: 
                desc = t.get('description', '') if isinstance(t, dict) else str(t)
                done = t.get('done', False) if isinstance(t, dict) else False
                self.add_list_item(self.trait_list, desc, t, done)

    def load_tasks(self):
        self.task_list.clear()
        if self.is_obj:
            if hasattr(self.data, '_temp_taches'):
                items = self.data._temp_taches
                for t in items:
                    self.add_list_item(self.task_list, t['description'], t, t['done'])
            else:
                items = self.data.taches
                for t in items:
                    self.add_list_item(self.task_list, t.description, t, t.done)
        else:
            items = self.data.get('taches', [])
            for t in items:
                desc = t.get('description', '') if isinstance(t, dict) else str(t)
                done = t.get('done', False) if isinstance(t, dict) else False
                self.add_list_item(self.task_list, desc, t, done)

    def add_list_item(self, list_widget, text, data, checked=False):
        item = QListWidgetItem(text)
        item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
        item.setCheckState(Qt.Checked if checked else Qt.Unchecked)
        item.setData(Qt.UserRole, data)
        list_widget.addItem(item)

    def add_traitement(self):
        text, ok = QInputDialog.getText(self, "Traitement", "Description:")
        if ok and text:
            self.add_list_item(self.trait_list, text, {"description": text, "done": False}, False)

    def del_traitement(self):
        self.trait_list.takeItem(self.trait_list.currentRow())

    def add_task(self):
        text, ok = QInputDialog.getText(self, "Tâche", "Description:")
        if ok and text:
            self.add_list_item(self.task_list, text, {"description": text, "done": False}, False)

    def del_task(self):
        self.task_list.takeItem(self.task_list.currentRow())

    def save(self):
        # Update self.data with new values
        name = self.name_edit.text()
        if not name: return
        
        vals = {
            'name': name,
            'info': self.info_edit.toPlainText(),
            'important_info': self.important_edit.toPlainText(),
            'cta_validated': self.chk_cta.isChecked(),
            'reparations_validated': self.chk_rep.isChecked(),
            'reparations_details': self.rep_details.toPlainText()
        }
        
        from datetime import date # Ensure import

        # Collect subtables with check state
        new_traitements = []
        for i in range(self.trait_list.count()):
            item = self.trait_list.item(i)
            userData = item.data(Qt.UserRole)
            # Update done state in dict/object-dict wrapper
            is_done = (item.checkState() == Qt.Checked)
            done_at = date.today() if is_done else None

            if isinstance(userData, dict):
                userData['done'] = is_done
                userData['done_at'] = done_at
            else:
                if hasattr(userData, 'description'):
                     userData = {"description": userData.description, "done": is_done, "done_at": done_at}
                else:
                     userData['done'] = is_done
                     userData['done_at'] = done_at
            new_traitements.append(userData)
            
        new_tasks = []
        for i in range(self.task_list.count()):
            item = self.task_list.item(i)
            userData = item.data(Qt.UserRole)
            is_done = (item.checkState() == Qt.Checked)
            done_at = date.today() if is_done else None

            if isinstance(userData, dict):
                userData['done'] = is_done
                userData['done_at'] = done_at
            else:
                if hasattr(userData, 'description'):
                     userData = {"description": userData.description, "done": is_done, "done_at": done_at}
                else:
                     userData['done'] = is_done
                     userData['done_at'] = done_at
            new_tasks.append(userData)

        if self.is_obj:
            for k, v in vals.items():
                setattr(self.data, k, v)
            # Sync lists (Simplified: we handle this in ActivityDialog save or we do it here if we had session)
            # We don't have session here easily without passing it.
            # Let's store temporary lists on the object to be processed by Activity Dialog
            self.data._temp_traitements = new_traitements
            self.data._temp_taches = new_tasks
        else:
            self.data.update(vals)
            self.data['traitements'] = new_traitements
            self.data['taches'] = new_tasks
            
        self.accept()

class ActivityDialog(QDialog):
    def __init__(self, activity_id=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Activité")
        self.setMinimumWidth(600)
        self.setMinimumHeight(500)
        
        self.activity_id = activity_id
        self.db = SessionLocal()
        
        self.layout = QVBoxLayout(self)
        
        # Formulaire principal
        form_layout = QFormLayout()
        self.name_edit = QLineEdit()
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.desc_edit = QTextEdit()
        self.desc_edit.setMaximumHeight(80)
        
        form_layout.addRow("Nom:", self.name_edit)
        form_layout.addRow("Date:", self.date_edit)
        form_layout.addRow("Description:", self.desc_edit)
        
        self.layout.addLayout(form_layout)
        
        # Section Scellés
        self.layout.addWidget(QLabel("<b>Scellés</b>"))
        self.scelles_list = QListWidget()
        self.layout.addWidget(self.scelles_list)
        
        scelle_btn_layout = QHBoxLayout()
        add_scelle_btn = QPushButton("Ajouter Scellé")
        add_scelle_btn.clicked.connect(self.add_scelle_dialog)
        edit_scelle_btn = QPushButton("Modifier Scellé")
        edit_scelle_btn.clicked.connect(self.edit_scelle_dialog)
        del_scelle_btn = QPushButton("Supprimer Scellé")
        del_scelle_btn.clicked.connect(self.delete_scelle)
        
        scelle_btn_layout.addWidget(add_scelle_btn)
        scelle_btn_layout.addWidget(edit_scelle_btn)
        scelle_btn_layout.addWidget(del_scelle_btn)
        self.layout.addLayout(scelle_btn_layout)
        
        # Tags (Simple visualization for now)
        self.layout.addWidget(QLabel("<b>Tags (séparés par virgule)</b>"))
        self.tags_edit = QLineEdit()
        self.layout.addWidget(self.tags_edit)

        # Buttons
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Enregistrer")
        save_btn.clicked.connect(self.save_activity)
        cancel_btn = QPushButton("Annuler")
        cancel_btn.clicked.connect(self.reject)
        
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        self.layout.addLayout(btn_layout)
        
        self.scelles_data = [] # Temporary storage for new scelles
        
        if self.activity_id:
            self.load_data()

    def load_data(self):
        activity = self.db.query(Activity).filter(Activity.id == self.activity_id).first()
        if activity:
            self.name_edit.setText(activity.name)
            self.date_edit.setDate(activity.date)
            self.desc_edit.setText(activity.description)
            tags_names = [t.name for t in activity.tags]
            self.tags_edit.setText(", ".join(tags_names))
            
            for sc in activity.scelles:
                self.add_scelle_to_list(sc)

    def add_scelle_to_list(self, scelle_obj_or_dict):
        item = QListWidgetItem()
        if isinstance(scelle_obj_or_dict, Scelle):
            text = f"{scelle_obj_or_dict.name} (ID: {scelle_obj_or_dict.id})"
            data = scelle_obj_or_dict
        else:
             text = f"{scelle_obj_or_dict['name']} (Nouveau)"
             data = scelle_obj_or_dict
        
        item.setText(text)
        item.setData(Qt.UserRole, data)
        self.scelles_list.addItem(item)

    def add_scelle_dialog(self):
        # Create empty dict structure
        scelle_data = {
            "name": "", "info": "", "important_info": "", 
            "cta_validated": False, "reparations_validated": False, "reparations_details": "",
            "traitements": [], "taches": []
        }
        dialog = ScelleDialog(scelle_data, self)
        if dialog.exec():
            # Apply changes to scelle_data (done in dialog)
            if scelle_data['name']:
                self.add_scelle_to_list(scelle_data)

    def edit_scelle_dialog(self):
        row = self.scelles_list.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Attention", "Veuillez sélectionner un scellé à modifier")
            return
            
        item = self.scelles_list.item(row)
        data = item.data(Qt.UserRole)
        
        dialog = ScelleDialog(data, self)
        if dialog.exec():
            # Refresh list item text
            name = data.name if isinstance(data, Scelle) else data['name']
            id_suffix = f" (ID: {data.id})" if isinstance(data, Scelle) else " (Nouveau)"
            item.setText(f"{name}{id_suffix}")
            # Data is already updated by reference in dialog

    def delete_scelle(self):
        row = self.scelles_list.currentRow()
        if row >= 0:
            item = self.scelles_list.item(row)
            data = item.data(Qt.UserRole)
            if isinstance(data, Scelle):
                # Mark for deletion
                self.db.delete(data)
            self.scelles_list.takeItem(row)

    def save_activity(self):
        name = self.name_edit.text()
        if not name:
            QMessageBox.warning(self, "Erreur", "Le nom est obligatoire")
            return

        cols = self.db.query(KanbanColumn).order_by(KanbanColumn.order_index).all()
        first_col = cols[0] if cols else None

        if self.activity_id:
            activity = self.db.query(Activity).filter(Activity.id == self.activity_id).first()
        else:
            activity = Activity()
            activity.column_id = first_col.id if first_col else None
        
        activity.name = name
        activity.date = self.date_edit.date().toPython()
        activity.description = self.desc_edit.toPlainText()
        
        self.db.add(activity)
        self.db.flush() # get ID
        
        # Tags processing
        tag_names = [t.strip() for t in self.tags_edit.text().split(",") if t.strip()]
        activity.tags = []
        for t_name in tag_names:
            tag = self.db.query(Tag).filter(Tag.name == t_name).first()
            if not tag:
                tag = Tag(name=t_name)
                self.db.add(tag)
            activity.tags.append(tag)

        # Scelles processing
        for i in range(self.scelles_list.count()):
            item = self.scelles_list.item(i)
            data = item.data(Qt.UserRole)
            
            scelle_model = None
            traitements_data = []
            taches_data = []
            
            if isinstance(data, dict):
                # New Scelle
                scelle_model = Scelle(
                    name=data['name'], 
                    info=data.get('info', ''),
                    important_info=data.get('important_info', ''),
                    cta_validated=data.get('cta_validated', False),
                    reparations_validated=data.get('reparations_validated', False),
                    reparations_details=data.get('reparations_details', ''),
                    activity_id=activity.id
                )
                traitements_data = data.get('traitements', [])
                taches_data = data.get('taches', [])
                self.db.add(scelle_model)
                self.db.flush() # get ID for relations
                
            elif isinstance(data, Scelle):
                # Existing Scelle - fields already updated by ref, but check for sub-lists
                scelle_model = data
                
                # Check if we have temp lists from dialog
                if hasattr(data, '_temp_traitements'):
                    # Replace all mappings. 
                    # Note: This is destructive but simple.
                    # Delete existing relations
                    self.db.query(Traitement).filter(Traitement.scelle_id == scelle_model.id).delete()
                    traitements_data = data._temp_traitements
                    delattr(data, '_temp_traitements')
                else:
                    # No changes to sub-items
                    # But wait, if user opened dialog, _temp exists. If not, we shouldn't touch it.
                    # We only need to "keep" existing if no edit happened. 
                    # Actually if edit didn't happen, _temp won't exist, so we do nothing, which is correct.
                    pass
                    
                if hasattr(data, '_temp_taches'):
                    self.db.query(Tache).filter(Tache.scelle_id == scelle_model.id).delete()
                    taches_data = data._temp_taches
                    delattr(data, '_temp_taches')

            # Process Sub-items (if scelle_model is valid and we have data to write)
            if scelle_model:
                for t_data in traitements_data:
                    # t_data is now ensured to be a dict by ScelleDialog.save()
                    # or it came from dict init.
                    # Safety check
                    desc = t_data.get('description', '') if isinstance(t_data, dict) else str(t_data)
                    is_done = t_data.get('done', False) if isinstance(t_data, dict) else False
                    done_at = t_data.get('done_at', None) if isinstance(t_data, dict) else None
                    
                    new_t = Traitement(description=desc, done=is_done, done_at=done_at, scelle_id=scelle_model.id)
                    self.db.add(new_t)
                    
                for tk_data in taches_data:
                    desc = tk_data.get('description', '') if isinstance(tk_data, dict) else str(tk_data)
                    is_done = tk_data.get('done', False) if isinstance(tk_data, dict) else False
                    done_at = tk_data.get('done_at', None) if isinstance(tk_data, dict) else None
                    
                    new_tk = Tache(description=desc, done=is_done, done_at=done_at, scelle_id=scelle_model.id)
                    self.db.add(new_tk)
        
        self.db.commit()
            
        self.accept()
    
    def closeEvent(self, event):
        self.db.close()
        super().closeEvent(event)
