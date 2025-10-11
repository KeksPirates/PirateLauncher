import aria2p
import subprocess
from core.utils.data.state import state
from plyer import notification
import time

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
    
    aria2server = subprocess.Popen(cmd)
    return aria2server

def dlprogress():
    try:
        downloads = state.aria2.get_downloads()
        if downloads:
            for download in downloads:
                progress = download.progress_string(0)
                progress_int = int(progress.strip('%'))
                return progress_int
        return 0
    except:
        return 0

def send_notification():
    while True:
        try:
            for d in state.aria2.get_downloads():
                if dlprogress() == 100:
                        notification.notify(
                            title="Download finished",
                            message=f"{d.name} has finished downloading.",
                            timeout=4
                        )
        except Exception as e:
            if state.debug:
                print("Notification thread error:", e)
        time.sleep(5)
