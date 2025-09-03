from core.ui.gui import MainWindow
from PySide6 import QtWidgets
import qdarktheme
import darkdetect
import sys

def run_gui():
    app = QtWidgets.QApplication([])
    if darkdetect.isDark:
        app.setStyleSheet(qdarktheme.load_stylesheet("dark"))
    else:
        app.setStyleSheet(qdarktheme.load_stylesheet("light"))
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run_gui()
