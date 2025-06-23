import requests
from bs4 import BeautifulSoup

url = "https://uztracker.net/viewtopic.php?t=23897"
response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    maintitle = soup.find(class_='tt-text')
    if maintitle:
        print("Program found:", maintitle.text) 

    else:
        print("Program not found")