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
    
    return aria2

t = 4 # default value

def set_threads(threads):
    global t
    t = threads




def aria2server():
    downloads_dir = os.path.join("Library")

    cmd = [
        "aria2c",
        "--enable-rpc",
        "--disable-ipv6", # added this since it caused problems with vpns
        "--rpc-listen-all",
        "--rpc-listen-port=6800",
        f"--dir={downloads_dir}",
        "-x", str(t),
        "-s", str(t),
    ]


    
    aria2server = subprocess.Popen(cmd)
    return aria2server
