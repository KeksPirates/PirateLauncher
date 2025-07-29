import aria2p
import os
import subprocess


def run_aria2p():

    aria2 = aria2p.API(
        aria2p.Client(
            host="http://localhost",
            port=6800,
            secret=""
        )
    )


    downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
    subprocess.Popen(["aria2c", "--enable-rpc", "--rpc-listen-all=true", f"--dir={downloads_dir}"])

    
    return aria2