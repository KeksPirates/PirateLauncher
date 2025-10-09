import requests
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from core.utils.data.state import state


global url_uztracker
url_uztracker = "https://uztracker.net/tracker.php?nm="

async def init_uztracker():
    global up
    global soup
    try:
        response = requests.get(url_uztracker, timeout=10)
        if response.status_code == 200:
            up = True
        else:
            up = False
            print(f"Uztracker seems down, status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"\nRequest Exception on {url_uztracker}:")
        print(e)
        print("\nIs the Site down?")
        up = False

asyncio.run(init_uztracker())

async def scrape_uztracker(search, max_results=450):
    if up:
        result = False
        global results
        global resulttitles
        results = [] 
        resulttitles = []

        per_page = 50

        for start in range(0, max_results, per_page):
            search_url = url_uztracker + search + f"&start={start}"
            if state.debug:
                print(search_url)

            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(search_url) as response:
                        response.raise_for_status()
                        text = await response.text()
                        soup = BeautifulSoup(text, 'html.parser')
                        links = soup.find_all('a', class_="genmed tLink", href=lambda x: x and x.startswith('./viewtopic'))
                        resultCount = 0
                        for link in links:
                            if link.b:
                                resultCount += 1
                                results.append(link['href'])
                                resulttitles.append(link.b.text)
                                result = True
                        
                        if resultCount == 0:
                            # add popup in gui for no result
                            break
                        
                except aiohttp.ClientError as e:
                    if result:
                        print(f"Failed to fetch {search_url}: {e}")
                    return None

        else:
            print("Error: Uztracker down")
            return None, None

        if not results:
            return None, None

        return resulttitles, results

def get_post_title(post_url):
    if up:
        response = requests.get(post_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        maintitle = soup.find(class_='tt-text')
        if maintitle:
            return maintitle.text
        else:
            if state.debug:
                print("Program not found")
    else:
        print("Error: Uztracker down")
        return None   

    


