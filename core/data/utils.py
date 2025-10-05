import requests
from bs4 import BeautifulSoup


def get_magnet_link(post_url, debug):
    try:
        response = requests.get(post_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        magnet_link = soup.find('a', href=lambda x: x and x.startswith('magnet:'))
        if magnet_link:
            if debug:
                print("Magnet Link Retrieved: ", magnet_link['href'])
            return magnet_link['href']
        else:
            if debug:
                print("Magnet Link not Found!")
    except requests.RequestException as e:
        if debug:
            print(f"Failed to fetch {post_url}: {e}")
        return None