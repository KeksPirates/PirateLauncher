import requests
from bs4 import BeautifulSoup
from core.utils.data.state import state
from core.utils.network.jsonhandler import format_data



def get_item_url(item, posts, post_titles): # softwarelist currentitem, post list (dict), post titles list
        post_index = post_titles.index(item)
        if 0 <= post_index < len(post_titles): 
            if state.tracker == "uztracker":
                item = "https://uztracker.net/" + state.post_urls[post_index].lstrip("./")
                if state.debug: 
                    print("Found post URL: ", item)
                return item
            if state.tracker == "rutracker":                
                item_dict = posts[post_index]
                _, post_links, _ = format_data([item_dict])
                if state.debug: 
                    print("Found post URL: ", post_links[0])
                return post_links[0]

        return None



def get_magnet_link(post_url):
    try:
        response = requests.get(post_url) # eventually impl. cloudscraper
        if state.debug:
            print("Sent Request to retrieve Magnet Link...")
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        magnet_link = soup.find('a', href=lambda x: x and x.startswith('magnet:'))
        if magnet_link:
            if state.debug:
                print("Magnet Link Retrieved: ", magnet_link['href'])
            return magnet_link['href']
        else:
            if state.debug:
                print("Magnet Link not Found!")
    except requests.RequestException as e:
        if state.debug:
            print(f"Failed to fetch {post_url}: {e}")
        return None
    
