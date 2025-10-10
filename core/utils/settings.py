from core.utils.data.state import state
import os
import platform

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

def save_settings(thread_count, close, apiurl):
    if platform.system() == "Windows":
        config_dir = os.environ.get("APPDATA", os.path.expanduser("~\\AppData\\Roaming"))
    else:
        config_dir = os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
    settings_path = os.path.join(config_dir, "SoftwareManager")
    os.makedirs(settings_path, exist_ok=True)

    with open(os.path.join(settings_path, "config.yml"), 'w') as f:
        f.write(f"aria2_threads: {state.aria2_threads}\n")
        f.write(f"api_url: {state.api_url}\n")

    state.aria2_threads = thread_count
    state.api_url = apiurl
    restart_aria2c()

    close()
