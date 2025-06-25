import requests
from bs4 import BeautifulSoup
import curses

search = input("Enter the name of the program you want to search for: ")
url = "https://uztracker.net/tracker.php?nm=" # placeholder url for now
response = requests.get(url) # get da content from da url
soup = BeautifulSoup(response.content, 'html.parser') # create bs object

def scrape_uztracker():
    search_url = url + search
    print(search_url)
    try:
        response = requests.get(search_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a')
        found_links = False
        for link in links:
            if link.has_attr('href'):
                href = link['href']
                post_url = f"https:{href}" if isinstance(href, str) and href.startswith("//") else href
                if isinstance(post_url, str) and post_url.startswith("./viewtopic.php?t="):
                    post_url = f"https://uztracker.net{post_url[1:]}"
                    print(f"Found post link: {post_url}")
                    found_links = True
        if not found_links:
            print(f"No post link found on {search_url}")
        return soup
    except requests.RequestException as e:
        print(f"Failed to fetch {search_url}: {e}")
        return None

def get_post_title(soup):
    maintitle = soup.find(class_='tt-text')
    if maintitle:
        print("Program found:", maintitle.text) 
    else:
        print("Program not found")

def get_magnet_link(post_url="https://uztracker.net/viewtopic.php?t=23897"):
    try:
        response = requests.get(post_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        magnet_link = soup.find('a', href=lambda x: x and x.startswith('magnet:'))
        if magnet_link:
            print("Magnet Link found:", magnet_link['href'])
        else:
            print("Magnet Link not Found!")
    except requests.RequestException as e:
        print(f"Failed to fetch {post_url}: {e}")

  # What x and x.startswith('magnet:') Does

  # x - check if x exists (not None/empty)
  # and - if x exists, THEN check the next part
  # x.startswith('magnet:') - does x start with "magnet:"?

post_url = scrape_uztracker

if __name__ == "__main__":
    soup = scrape_uztracker()
    if soup:
        get_post_title(soup)
        get_magnet_link()
    
