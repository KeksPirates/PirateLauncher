import requests

server = "https://pizzasucht.net"


def scrape_rutracker(search_text):
    search = requests.get(f"{server}/search/{search_text}")
    data = search.json()
    resulttitles = data["titles"]
    resultlinks = data["links"]
    return resulttitles, resultlinks


# This Function utilizes the SoftwareManager Server - Source Code can be found in the "Server" branch.