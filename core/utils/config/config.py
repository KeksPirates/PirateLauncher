import os
import platform
import configparser
from core.utils.data.state import state


def create_config():
    config = configparser.ConfigParser()

    config["General"] = {"debug": True, "api_url": f"{state.api_url}", "aria2_threads": f"{state.aria2_threads}", "download_path": f"{state.download_path}"}

    if platform.system() == "Windows":
            config_dir = os.environ.get("APPDATA", os.path.expanduser("~\\AppData\\Roaming"))
    else:
        config_dir = os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))

    settings_path = os.path.join(config_dir, "SoftwareManager")
    os.makedirs(settings_path, exist_ok=True)

    with open(os.path.join(settings_path, "config.yml"), 'w') as cf:
        config.write(cf)


def read_config():

    config = configparser.ConfigParser()

    if platform.system() == "Windows":
            config_dir = os.environ.get("APPDATA", os.path.expanduser("~\\AppData\\Roaming"))
    else:
        config_dir = os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
    settings_path = os.path.join(config_dir, "SoftwareManager")
    config_file = os.path.join(settings_path, "config.yml")

    if not os.path.exists(config_file):
        create_config()

    config.read(config_file)

    state.debug = config.getboolean("General", "debug")
    state.api_url = config.get("General", "api_url")
    state.aria2_threads = config.getint("General", "aria2_threads")
    state.download_path = config.get("General", "download_path")

