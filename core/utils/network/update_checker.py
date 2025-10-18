import requests
from core.utils.data.state import state

def check_for_updates():
    url = f"https://api.github.com/repos/KeksPirates/SoftwareManager/releases"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to fetch releases: {response.status_code}")
        exit(1)

    releases = response.json()
    releases.sort(key=lambda r: r["published_at"], reverse=True)

    latest_release = releases[0]
    latest_version = latest_release["name"]
    assets = latest_release["assets"]

    if latest_version != state.version:
        if state.debug:
            print(f"New release available: {latest_version}")
        if assets:
            if state.debug:
                print("Assets:")
                for asset in assets:
                    print(f" - {asset['name']}: {asset['browser_download_url']}")
            return assets, latest_version
    else:
        if state.debug:
            print("Already up-to-date.")
        return None, None
