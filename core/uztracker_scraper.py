import requests
from bs4 import BeautifulSoup

search = input("Enter the name of the program you want to search for: ")
url = "https://uztracker.net/tracker.php?nm=" # placeholder url for now
response = requests.get(url) # get da content from da url
soup = BeautifulSoup(response.content, 'html.parser') # create bs object

def scrape_uztracker():
    search_url = url + search
    print(search_url)
    result = False
    try:
        response = requests.get(search_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', class_="genmed tLink", href=lambda x: x and x.startswith('./viewtopic'))
        for link in links:
            if link.b:
                print("Result found:", link.b.text, "|", link['href'])
                result = True
                
        if not result:
            print(f'No Results found for "{search}"')
            
        return soup
    except requests.RequestException as e:
        print(f"Failed to fetch {search_url}: {e}")
        return None

def get_post_title(post_url):
    soup = BeautifulSoup(response.text, 'html.parser')
    maintitle = soup.find(class_='tt-text')
    if maintitle:
        print(maintitle.text) 
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




if __name__ == "__main__":
    soup = scrape_uztracker()
    
