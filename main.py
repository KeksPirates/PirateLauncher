from core.ui.gui import MainWindow
from core.ui.gui import state_debug
from core.downloading.aria2p_server import aria2server
from PySide6 import QtWidgets
import qdarktheme
import darkdetect
import subprocess
import signal
import atexit
import sys

debug = True
aria2process = None

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

def kill_aria2server():
    global aria2process
    if aria2process:
        aria2process.kill()
        if debug:
            print("\nKilled Aria2")

def keyboardinterrupthandler(signum, frame):
    kill_aria2server()
    sys.exit(0)



if __name__ == "__main__":
    kill_aria2server()
    if debug:
        print("Starting Aria2 Server")
    aria2process = aria2server()
    signal.signal(signal.SIGINT, keyboardinterrupthandler)
    atexit.register(kill_aria2server)
    if debug:
        print("Launching GUI")
    run_gui()
