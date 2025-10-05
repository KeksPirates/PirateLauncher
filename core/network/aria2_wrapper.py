from .aria2_integration import run_aria2p

def start_client():
    global aria2
    aria2 = run_aria2p()

def add_magnet(uri):
    aria2.add_magnet(uri)


def terminate():
    return




