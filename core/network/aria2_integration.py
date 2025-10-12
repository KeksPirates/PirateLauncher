import aria2p
import subprocess
from core.utils.data.state import state
from plyer import notification
import time
import sys

def run_aria2p():

    state.aria2 = aria2p.API(
        aria2p.Client(
            host="http://localhost",
            port=6800,
            secret=""
        )
    )
    
    return state.aria2


def aria2server():
    download_path = state.download_path
    speed_limit = state.speed_limit

    cmd = [
        "aria2c",
        "--enable-rpc",
        "--disable-ipv6", # added this since it caused problems with vpns
        "--rpc-listen-all",
        "--rpc-listen-port=6800",
        f"--dir={download_path}",
        f"--max-download-limit={speed_limit * 1024}",
        "-x", str(state.aria2_threads),
        "-s", str(state.aria2_threads),
    ]
    
    aria2server = subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
    )
    return aria2server

def dlprogress():
    try:
        state.downloads = [download for download in state.aria2.get_downloads() if not download.is_metadata]
        downloads = state.downloads
        if downloads:
            for download in downloads:
                progress = download.progress_string(0)
                progress_int = int(progress.strip('%'))
                return progress_int
        return 0
    except:
        return 0

def send_notification(shutdown_event):
    while not shutdown_event.is_set():
        try:
            for download in state.downloads:
                if dlprogress() == 100:
                        notification.notify(
                            title = "Download finished",
                            message = f"{download.name} has finished downloading.",
                            timeout = 4
                        )
        except Exception as e:
            pass
        time.sleep(5)
