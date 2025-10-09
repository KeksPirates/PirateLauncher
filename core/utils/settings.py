from core.network.aria2_integration import set_threads


def restart_aria2c(aria2process):
        import main # had to do this because of circle import :(
        import signal
        import atexit
        main.kill_aria2server(aria2process)
        aria2process.wait()
        aria2process = main.run_aria2server()
        signal.signal(signal.SIGINT, main.keyboardinterrupthandler)
        atexit.unregister(main.kill_aria2server)
        atexit.register(main.kill_aria2server, aria2process)

def save_settings(thread_count, close, apiurl, aria2process):
    global api_url
    set_threads(thread_count)
    api_url = apiurl
    restart_aria2c(aria2process)
    close()