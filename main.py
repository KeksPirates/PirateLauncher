from core.interface.gui import MainWindow
from core.utils.data.state import state
from core.network.aria2_integration import aria2server
from PySide6 import QtWidgets
import qdarktheme
import darkdetect
import signal
import atexit
import sys

# Debug Output
state.debug = True

def run_gui():
    app = QtWidgets.QApplication([])
    if darkdetect.isDark:
        app.setStyleSheet(qdarktheme.load_stylesheet("dark"))
    else:
        app.setStyleSheet(qdarktheme.load_stylesheet("light"))
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())

def run_aria2server():
    global aria2process
    aria2process = aria2server()
    return aria2process


def kill_aria2server():
    if state.aria2process:
        state.aria2process.kill()
        if state.debug:
            print("\nKilled Aria2")


def keyboardinterrupthandler(signum, frame):
    kill_aria2server()
    sys.exit(0)


if __name__ == "__main__":
    if state.debug:
        print("Starting Aria2 Server")
    state.aria2process = run_aria2server()
    signal.signal(signal.SIGINT, keyboardinterrupthandler)
    atexit.register(kill_aria2server)
    if state.debug:
        print("Launching GUI")
    run_gui()
    
