from core.utils.data.state import state
import threading


shutdown_event = threading.Event()

def kill_aria2server():
    if state.aria2process:
        state.aria2process.kill()
        if state.debug:
            print("\nKilled Aria2")


def closehelper():
    shutdown_event.set()
    kill_aria2server()