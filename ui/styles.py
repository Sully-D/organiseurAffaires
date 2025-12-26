DARK_THEME = """
/* Tokyo Night Theme */
QWidget {
    background-color: #1a1b26;
    color: #c0caf5;
    font-family: 'Segoe UI', sans-serif;
    font-size: 14px;
}

QLineEdit, QTextEdit, QDateEdit, QComboBox {
    background-color: #16161e;
    border: 1px solid #565f89;
    border-radius: 4px;
    padding: 5px;
    color: #c0caf5;
}

QPushButton {
    background-color: #7aa2f7;
    color: #1a1b26;
    font-weight: bold;
    border: none;
    border-radius: 4px;
    padding: 6px 12px;
}

QPushButton:hover {
    background-color: #7dcfff;
}

QPushButton:pressed {
    background-color: #3d59a1;
}

/* Kanban Column */
QFrame#KanbanColumn {
    background-color: #16161e;
    border: 1px solid #1a1b26;
    border-radius: 8px;
    padding: 10px;
}

/* Activity Card */
QFrame#ActivityCard {
    background-color: #24283b;
    border-radius: 6px;
    border: 1px solid #414868;
    margin-bottom: 8px;
}

QFrame#ActivityCard[overdue="true"] {
    border: 2px solid #f7768e; /* Tokyo Night Red */
}

QFrame#ActivityCard:hover {
    border: 1px solid #7aa2f7;
}

/* Scelle Frame (Inner) */
QFrame.ScelleFrame {
    background-color: #1f2335;
    border-radius: 4px;
    margin-top: 2px;
}

QLabel#ColumnTitle {
    font-size: 16px;
    font-weight: bold;
    color: #7aa2f7;
    margin-bottom: 10px;
}

QLabel#CardTitle {
    font-weight: bold;
    font-size: 15px;
    color: #bb9af7;
}

QLabel.BadgeImportant {
    background-color: #f7768e;
    color: #15161e;
    border-radius: 4px;
    padding: 2px 5px;
    font-weight: bold;
    font-size: 11px;
    margin-right: 5px;
}

QLabel.BadgeCTA {
    background-color: #9ece6a;
    color: #15161e;
    border-radius: 4px;
    padding: 2px 5px;
    font-size: 11px;
    margin-right: 5px;
}

QLabel.BadgeRep {
    background-color: #ff9e64;
    color: #15161e;
    border-radius: 4px;
    padding: 2px 5px;
    font-size: 11px;
    margin-right: 5px;
}

QLabel.ScelleName {
    font-weight: bold;
    color: #565f89;
}
"""
