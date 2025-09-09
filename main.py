from core.ui.gui import MainWindow
from core.ui.gui import state_debug

from PySide6 import QtWidgets
import qdarktheme
import darkdetect
import sys

debug = True

def run_gui():
    state_debug(debug)
    app = QtWidgets.QApplication([])
    if darkdetect.isDark():
        app.setStyleSheet(qdarktheme.load_stylesheet("dark"))
    else:
        app.setStyleSheet(qdarktheme.load_stylesheet("light"))
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    run_gui()
