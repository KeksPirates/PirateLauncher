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
            
        select_program()
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

def select_program():
    selection = input("Enter the Number of the Program you want to download: ")
    try:
        index = int(selection) - 1
        if 0 <= index < len(results): # note for myself: py starts counting at 0; check if number is not negative, check if number is not more than list length.
            selected = "https://uztracker.net/" + results[index].lstrip("./")
            post_url = selected
            get_magnet_link(post_url)

    except ValueError:
        print("Invalid Selection.")
        return

def get_magnet_link(post_url):
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
    
    
