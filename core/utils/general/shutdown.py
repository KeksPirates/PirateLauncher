from core.utils.data.state import state
import threading
import psutil
import sys


shutdown_event = threading.Event()

def kill_aria2server():
    if sys.platform.startswith("win"):
        process = "aria2c.exe"
    else:
        process = "aria2c"

    if state.aria2process:
        state.aria2process.kill()
        if state.debug:
            print("Killed Aria2")

    for proc in psutil.process_iter():
        if proc.name() == process:
            proc.kill()
            if state.debug:
                print("Killed Aria2c")


def closehelper():
    shutdown_event.set()
    kill_aria2server()