import requests

server = "https://api.michijackson.xyz"


def scrape_rutracker(search_text, debug):
    search = requests.get(f"{server}/search/{search_text}")
    if search:
        try:
            data = search.json()
            resulttitles = data["titles"]
            resultlinks = data["links"]
            return resulttitles, resultlinks
        except Exception:
            if debug:
                print("No results found / No response from server")
            return None

    else:
        return None
        


# This function utilizes the SoftwareManager server - source code can be found under the "server" branch.
