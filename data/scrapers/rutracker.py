import cloudscraper
import requests
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv


global url_rutracker
url_rutracker = "https://rutracker.org/forum/tracker.php?nm="


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
        response = scraper.get(url_rutracker, cookies=cookies, headers=headers)
        if response.status_code == 200:
            up = True
        else:
            up = False
            print(f"Rutracker seems down, status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"\nRequest Exception on {url_rutracker}:")
        print(e)
        print("\nIs the Site down?")
        up = False

def scrape_rutracker(search_term, max_results = 450):
    if up:
        result = False
        global results
        global resulttitles
        results = []
        resulttitles = []

        per_page = 50

        for start in range(0, max_results, per_page):
            search_url = url_rutracker + search_term + f"&start={start}"
            print(search_url)

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
                        results.append(link['href'])
                        resulttitles.append(link.text)
                        result = True

                if resultCount == 0:
                    break

            except requests.RequestException as e:
                if result:
                    print(f"Failed to fetch {search_url}: {e}")
                return "error"

        if not results:
            return None, None

        return {"links": ["https://rutracker.org/forum/" + r for r in results], "titles": resulttitles}

    else:
        print("Error: Rutracker down")
        return "Error: Rutracker down"
