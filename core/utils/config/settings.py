from core.utils.data.state import state
from .config import create_config

def restart_aria2c():
    import main # had to do this because of circle import :(
    import signal
    import atexit
    import time

    try:
        main.kill_aria2server()
    except Exception as e:
        print(f"Warning: aria2server kill failed: {e}")

    try:
        if state.aria2process:
            state.aria2process.wait(timeout=3)
    except Exception as e:
        print(f"Warning: aria2process wait failed: {e}")

    time.sleep(0.5)

    try:
        state.aria2process = main.run_aria2server()
    except Exception as e:
        print(f"Error: failed to restart aria2server: {e}")
        return

    try:
        signal.signal(signal.SIGINT, main.keyboardinterrupthandler)
        atexit.unregister(main.kill_aria2server)
        atexit.register(main.kill_aria2server)
    except Exception as e:
        print(f"Warning: signal/atexit setup failed: {e}")

def save_settings(thread_count=None, close=lambda: None, apiurl=None, download_path=None, speed_limit=None, version=None):
    if thread_count is not None:
        state.aria2_threads = thread_count
    if apiurl is not None:
        state.api_url = apiurl
    if download_path is not None:
        state.download_path = download_path
    if speed_limit is not None:
        state.speed_limit = speed_limit
    if version is not None:
        state.version = version
    
    create_config()
    restart_aria2c()
    close()
