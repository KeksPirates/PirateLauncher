from core.utils.data.state import state
from .config import create_config

def restart_aria2c():
    import main # had to do this because of circle import :(
    import signal
    import atexit
    main.kill_aria2server()
    state.aria2process.wait()
    state.aria2process = main.run_aria2server()
    signal.signal(signal.SIGINT, main.keyboardinterrupthandler)
    atexit.unregister(main.kill_aria2server)
    atexit.register(main.kill_aria2server)

def save_settings(thread_count, close, apiurl, download_path, speed_limit):
    state.aria2_threads = thread_count
    state.api_url = apiurl
    state.download_path = download_path
    state.speed_limit = speed_limit
    
    create_config()
    restart_aria2c()
    close()
