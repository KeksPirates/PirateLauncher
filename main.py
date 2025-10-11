from core.interface.gui import MainWindow
from core.utils.data.state import state
from core.network.aria2_integration import aria2server
from core.network.aria2_integration import send_notification
from core.utils.wrappers import run_thread
import threading
from core.utils.config.config import read_config
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
    read_config()
    if state.debug:
        print("Starting Aria2 Server")
    state.aria2process = run_aria2server()
    signal.signal(signal.SIGINT, keyboardinterrupthandler)
    atexit.register(kill_aria2server)
    run_thread(threading.Thread(target=send_notification))
    if state.debug:
        print("Launching GUI")
    run_gui()

