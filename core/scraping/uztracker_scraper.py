import requests
from bs4 import BeautifulSoup

global url_uztracker
global up
url_uztracker = "https://uztracker.net/tracker.php?nm=" # placeholder url for now
try:
    response = requests.get(url_uztracker) # get da content from da url
    soup = BeautifulSoup(response.content, 'html.parser') # create bs object
    up = True
except requests.exceptions.RequestException as e:
    print(f"\nRequest Exception on {url_uztracker}:")
    print(e)
    print("\nIs the Site down?")
    up = False

def scrape_uztracker(search, debug):
    if up:
        search_url = url_uztracker + search
        if debug:
            print(search_url)
        result = False
        global results
        global resulttitles
        results = []
        resulttitles = []

        try:
            resultCount = 0
            response = requests.get(search_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a', class_="genmed tLink", href=lambda x: x and x.startswith('./viewtopic'))
            for link in links:
                if link.b:
                    resultCount += 1
                    
                    # print(f"Result found: ({resultCount}) {link.b.text} | {link['href']}")
                    results.append(link['href'])
                    resulttitles.append(link.b.text)
                    result = True
                    
            if result:
                return resulttitles, results
                    
            if not result:
                if debug:
                    print(f'No Results found for "{search}"')
                # add popup in gui for no result
                return
            
        except requests.RequestException as e:
            if result:
                print(f"Failed to fetch {search_url}: {e}")
            return None
    else:
        print("Error: Uztracker down")
        return None, None    

def get_post_title(post_url, debug):
    if up:
        response = requests.get(post_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        maintitle = soup.find(class_='tt-text')
        if maintitle:
            return maintitle.text
        else:
            if debug:
                print("Program not found")
    else:
        print("Error: Uztracker down")
        return None   

    
def get_magnet_link(post_url, debug):
    if up:
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
    else:
        print("Error: Uztracker down") 
        return None

# What x and x.startswith('magnet:') Does
# x - check if x exists (not None/empty)
# and - if x exists, THEN check the next part
# x.startswith('magnet:') - does x start with "magnet:"?
    
