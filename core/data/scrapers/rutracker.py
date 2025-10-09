import requests
from ..utils.state import state


def scrape_rutracker(search_text):
    search = requests.get(f"{state.api_url}/search/{search_text}")
    if search:
        try:
            data = search.json()
            resulttitles = data["titles"]
            resultlinks = data["links"]
            return resulttitles, resultlinks
        except Exception:
            if state.debug:
                print("No results found / No response from server")
            return None

    else:
        return None
        


# This function utilizes the SoftwareManager server - source code can be found under the "server" branch.
