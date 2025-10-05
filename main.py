from core.interface.gui import MainWindow
from core.interface.gui import state_debug
from core.interface.gui import pass_aria
from core.network.aria2_integration import aria2server
from PySide6 import QtWidgets
import qdarktheme
import darkdetect
import signal
import atexit
import sys

debug = True

def run_gui():
    state_debug(debug)
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


def kill_aria2server(aria2process):
    if aria2process:
        aria2process.kill()
        if debug:
            print("\nKilled Aria2")


def keyboardinterrupthandler(signum, frame):
    global aria2process
    kill_aria2server(aria2process)
    sys.exit(0)


if __name__ == "__main__":
    if debug:
        print("Starting Aria2 Server")
    aria2process = run_aria2server()
    signal.signal(signal.SIGINT, keyboardinterrupthandler)
    atexit.register(kill_aria2server, aria2process)
    if debug:
        print("Launching GUI")

    pass_aria(aria2process)
    run_gui()
    
