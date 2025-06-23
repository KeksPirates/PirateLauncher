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



if response.status_code == 200:
    get_post_title()
    