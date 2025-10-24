import requests
from core.utils.data.state import state


def scrape_rutracker(search_text):
    search = requests.get(f"{state.api_url}/search/{search_text}")
    if state.debug:
        print("Sent request to server")
    if search:
        try:
            return search.text
        except Exception:
            if state.debug:
                print("No results found / No response from server")
            return None

    else:
        return None
        


# This function utilizes the SoftwareManager server - source code can be found under the "server" branch.
