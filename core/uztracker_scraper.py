import requests
from bs4 import BeautifulSoup

url = "https://uztracker.net/viewtopic.php?t=23897" # placeholder url for now
response = requests.get(url) # get da content from da url
soup = BeautifulSoup(response.content, 'html.parser') # create bs object

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

if response.status_code == 200:
    get_post_title()
    get_magnet_link()
    