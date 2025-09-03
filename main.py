from core.gui import run_gui as gui
from core.gui import MainWindow
from PySide6 import QtWidgets
import sys





def run_gui():
    app = QtWidgets.QApplication([])
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())



if __name__ == "__main__":
    run_gui()
