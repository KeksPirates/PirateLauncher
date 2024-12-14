import aria2p
import subprocess
import keyboard
import os

aria2 = aria2p.API(
    aria2p.Client(
        host="http://localhost",
        port=6800,
        secret=""
    )
)
download_paused = False
def pauseDownload(_):
    global download_paused
    if download_paused == True:
       print("Error: Download already paused.") 
    print("Download is being paused...")
    download_paused = True
    aria2.pause_all()

def startDownload(_):
    if download_paused == True:
        aria2.resume_all()
        print("Download Resumed!")
        download_paused = False
    print("Download Started!")
    download = aria2.add_magnet(magnet_uri)
    

downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")

subprocess.Popen(["aria2c", "--enable-rpc", "--rpc-listen-all=true", f"--dir={downloads_dir}"])

downloads = aria2.get_downloads()

for download in downloads:
    print(download.name, downloads.download_speed, download.status)
    
magnet_uri = "magnet:?xt=urn:btih:7FBF03CCC9115260DC50102E5A31E83E91422A79&dn=Ready+or+Not%3A+LSPD+Bundle+%28v66884+%2B+4+DLCs%2FBonuses+%2B+Windows+7+Fix%2C+MULTi12%29+%5BFitGirl+Repack%2C+Selective+Download+-+from+34.7+GB%5D&tr=udp%3A%2F%2Fopentor.net%3A6969&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=udp%3A%2F%2Ftracker.theoks.net%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.ccp.ovh%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=http%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce&tr=https%3A%2F%2Ftracker.tamersunion.org%3A443%2Fannounce&tr=udp%3A%2F%2Fexplodie.org%3A6969%2Fannounce&tr=http%3A%2F%2Ftracker.bt4g.com%3A2095%2Fannounce&tr=udp%3A%2F%2Fbt2.archive.org%3A6969%2Fannounce&tr=udp%3A%2F%2Fbt1.archive.org%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.filemail.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker1.bt.moack.co.kr%3A80%2Fannounce&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=http%3A%2F%2Ftracker.openbittorrent.com%3A80%2Fannounce&tr=udp%3A%2F%2Fopentracker.i2p.rocks%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.internetwarriors.net%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969%2Fannounce&tr=udp%3A%2F%2Fcoppersurfer.tk%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.zer0day.to%3A1337%2Fannounce"

keyboard.on_press_key("d", startDownload, suppress=False)
keyboard.on_press_key("s", pauseDownload, suppress=False)
keyboard.wait("q")
