import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    try:
        with open('theme.qss', 'r') as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        pass
        
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
