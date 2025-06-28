import requests
from bs4 import BeautifulSoup

global url_uztracker
url_uztracker = "https://uztracker.net/tracker.php?nm=" # placeholder url for now
response = requests.get(url_uztracker) # get da content from da url
soup = BeautifulSoup(response.content, 'html.parser') # create bs object

def scrape_uztracker():
    search = input("Enter the name of the program you want to search for: ")
    search_url = url_uztracker + search
    print(search_url)
    result = False
    global results
    results = []
    try:
        resultCount = 0
        response = requests.get(search_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', class_="genmed tLink", href=lambda x: x and x.startswith('./viewtopic'))
        for link in links:
            if link.b:
                resultCount += 1
                print(f"Result found: ({resultCount}) {link.b.text} | {link['href']}")
                results.append(link['href'])
                result = True
                
                
        if not result:
            print(f'No Results found for "{search}"')
            return
            
        selection = input("Enter the Number of the Program you want to download: ")


        try:
            index = int(selection) - 1
            if 0 <= index < len(results): # note for myself: py starts counting at 0; check if number is not negative, check if number is not more than list length.
                selected = "https://uztracker.net/" + results[index].lstrip("./")
                post_url = selected
                return selected
            else:
                print("Invalid Selection.")


        except ValueError:
            print(Exception)
            return

    except requests.RequestException as e:
        print(f"Failed to fetch {search_url}: {e}")
        return None

def get_post_title(post_url):
    response = requests.get(post_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    maintitle = soup.find(class_='tt-text')
    if maintitle:
        return maintitle.text
    else:
        print("Program not found")

    
def get_magnet_link(post_url):
    try:
        response = requests.get(post_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        magnet_link = soup.find('a', href=lambda x: x and x.startswith('magnet:'))
        if magnet_link:
            return magnet_link['href']
        else:
            print("Magnet Link not Found!")
    except requests.RequestException as e:
        print(f"Failed to fetch {post_url}: {e}")

  # What x and x.startswith('magnet:') Does

  # x - check if x exists (not None/empty)
  # and - if x exists, THEN check the next part
  # x.startswith('magnet:') - does x start with "magnet:"?




if __name__ == "__main__":
    selected = scrape_uztracker()
    maintitle = get_post_title(selected)
    magnetlink = get_magnet_link(selected)
    print(maintitle)
    print(magnetlink)
    
    
