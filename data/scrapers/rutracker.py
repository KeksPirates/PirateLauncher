import cloudscraper
import requests
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv




global url_rutracker
url_rutracker = "https://rutracker.org/forum/tracker.php?nm=" # placeholder url for now


load_dotenv()

scraper = cloudscraper.create_scraper()

cookies = {
    "bb_session": os.getenv("bb_session")
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:142.0) Gecko/20100101 Firefox/142.0"
}

def init():
    global up
    try:
        response = scraper.get(url_rutracker, cookies=cookies, headers=headers) # get da content from da url
        #print(response.content);
        soup = BeautifulSoup(response.content, 'html.parser') # create bs object
        up = True
    except requests.exceptions.RequestException as e:
        print(f"\nRequest Exception on {url_rutracker}:")
        print(e)
        print("\nIs the Site down?")
        up = False



def scrape_rutracker(search_term):
    if up:
        search_url = url_rutracker + search_term
        result = False
        global results
        global resulttitles
        results = []
        resulttitles = []
        try:
            resultCount = 0
            response = scraper.get(search_url, cookies=cookies, headers=headers)
            print(response.status_code)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a', class_="med tLink tt-text ts-text hl-tags bold", href=lambda x: x and x.startswith("viewtopic"))
            for link in links:
                if link:
                    resultCount += 1
                    # print(f"Result found: ({resultCount}) {link.b.text} | {link['href']}")
                    results.append(link['href'])
                    resulttitles.append(link.text)
                    result = True             
            if result:
                return {"links": ["https://rutracker.org/forum/" + r for r in results], "titles": resulttitles}
            if not result:
                # add popup in gui for no result
                return "no result"
        except requests.RequestException as e:
            if result:
                print(f"Failed to fetch {search_url}: {e}")
            return "error"
    else:
        print("Error: Rutracker down")
        return "Error: Rutracker down"