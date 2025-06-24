import requests
from bs4 import BeautifulSoup

search = input("Enter the name of the program you want to search for: ")
url = "https://uztracker.net/tracker.php?nm=" # placeholder url for now
response = requests.get(url) # get da content from da url
soup = BeautifulSoup(response.content, 'html.parser') # create bs object

def scrape_uztracker():
    search_url = url + search
    print(search_url)
    try:
        response = requests.get(search_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a')
        found_links = False
        for link in links:
            if link.has_attr('href'):
                href = link['href']
                post_url = f"https:{href}" if isinstance(href, str) and href.startswith("//") else href
                if isinstance(post_url, str) and post_url.startswith("https://uztracker.net/viewtopic.php?t="): # please figure out why this .startswith filter is not working
                    print(f"Found post link: {post_url}")
                    found_links = True
        if not found_links:
            print(f"No post link found on {search_url}")
        return soup
    except requests.RequestException as e:
        print(f"Failed to fetch {search_url}: {e}")
        return None

def get_post_title():
    maintitle = soup.find(class_='tt-text')
    if maintitle:
        print("Program found:", maintitle.text) 
    else:
        print("Program not found")


def get_magnet_link():
    magnet_link = soup.find('a', href=lambda x: x and x.startswith('magnet:')) # credits to claude for helping me with lambda. 
    if magnet_link:
        print("Magnet Link found:", magnet_link['href'])
    else:
        print("Magnet Link not Found!")

  # What x and x.startswith('magnet:') Does

  # x - check if x exists (not None/empty)
  # and - if x exists, THEN check the next part
  # x.startswith('magnet:') - does x start with "magnet:"?

if __name__ == "__main__":
    soup = scrape_uztracker()

if response.status_code == 200:
    get_post_title()
    get_magnet_link()
    
