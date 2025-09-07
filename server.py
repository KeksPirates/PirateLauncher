from flask import Flask
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

global url_rutracker
global up
url_rutracker = "https://rutracker.org/forum/tracker.php?nm=" # placeholder url for now

debug = False

cookies = {
    "bb_session": "YOUR_COOKIE"
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:142.0) Gecko/20100101 Firefox/142.0"
}

try:
    response = requests.get(url_rutracker, cookies=cookies, headers=headers) # get da content from da url
    #print(response.content);
    soup = BeautifulSoup(response.content, 'html.parser') # create bs object
    up = True
except requests.exceptions.RequestException as e:
    print(f"\nRequest Exception on {url_rutracker}:")
    print(e)
    print("\nIs the Site down?")
    up = False

@app.route('/search/<search_term>')
def search(search_term):
    return scrape_rutracker(search_term)

def scrape_rutracker(search_term):
    if up:
        search_url = url_rutracker + search_term
        if debug:
            print(search_url)
        result = False
        global results
        global resulttitles
        results = []
        resulttitles = []

        try:
            resultCount = 0
            response = requests.get(search_url, cookies=cookies, headers=headers)
            response.raise_for_status()
            # soup = BeautifulSoup(response.content, 'html.parser')

            # print(soup.prettify())
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
                if debug:
                    print(f'No Results found for "{search_term}"')
                # add popup in gui for no result
                return "no result"
            
        except requests.RequestException as e:
            if result:
                print(f"Failed to fetch {search_url}: {e}")
            return "error"
    else:
        print("Error: Rutracker down")
        return "Error: Rutracker down"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
