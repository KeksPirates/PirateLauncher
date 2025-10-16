from .aria2_integration import run_aria2p
from core.utils.data.state import state

def start_client():
    global aria2
    aria2 = run_aria2p()
    if state.debug:
        print("Started Aria2p")

def add_magnet(uri):
    aria2.add_magnet(uri)
    if state.debug:
        print("Magnet URI added to Aria2")



