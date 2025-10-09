import aria2p
import os
import subprocess
from core.utils.state import state

def run_aria2p():
    global aria2

    aria2 = aria2p.API(
        aria2p.Client(
            host="http://localhost",
            port=6800,
            secret=""
        )
    )
    
    return aria2




def aria2server():
    downloads_dir = os.path.join("Library")

    cmd = [
        "aria2c",
        "--enable-rpc",
        "--disable-ipv6", # added this since it caused problems with vpns
        "--rpc-listen-all",
        "--rpc-listen-port=6800",
        f"--dir={downloads_dir}",
        "-x", str(state.aria2_threads),
        "-s", str(state.aria2_threads),
    ]


    
    aria2server = subprocess.Popen(cmd)
    return aria2server

def dlprogress():
    try:
        download2 = aria2.get_downloads()
        if download2:
            for download in download2:
                progress = download.progress_string(0)
                progress_int = int(progress.strip('%'))
                return progress_int
        return 0
    except:
        return 0
