import requests
from bs4 import BeautifulSoup
from core.network.aria2_wrapper import start_client
from core.network.aria2_wrapper import add_magnet
from core.utils.data.state import state



def get_item_index(item, list, listlinks, debug):
        position = list.index(item)
        if 0 <= position < len(listlinks): # note for myself: py starts counting at 0; check if number is not negative, check if number is not more than list length.
            if state.tracker == "uztracker":
                selected = "https://uztracker.net/" + listlinks[position].lstrip("./")
            if state.tracker == "rutracker":                
                selected = listlinks[position]

            if debug:
                print("Selected URL: ", selected)
            selected_magnet = get_magnet_link(selected, debug)
            start_client()
            add_magnet(selected_magnet)




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
    
