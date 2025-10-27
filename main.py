import sys
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow
from version import __version__, __app_name__

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setApplicationName(__app_name__)
    app.setApplicationVersion(__version__)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
