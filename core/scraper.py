from bs4 import BeautifulSoup
import requests

badphrases = {}
badphrases.update({chr(i) for i in range(ord('A'), ord('Z') + 1)})

rutracker_url = "https://rutracker.org/forum/index.php"

def fetch_rutracker_software(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all("a")
        games_dict = {}
        for link in links:
            href = link.get("href", "").lower()
            text = link.text.strip()
            if text:
                games_dict[text] = href
        return games_dict
    else:
        print(f"Failed to retrieve the Rutracker page. Status code: {response.status_code}")
        return {}
