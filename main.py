import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from database.init_db import init_db

def main():
    # Ensure DB is initialized
    init_db()

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
