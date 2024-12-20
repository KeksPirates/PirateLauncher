from bs4 import BeautifulSoup
import requests
import re

url = "https://steamrip.com/games-list-page/"

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    links = soup.find_all("a")
    
    games_dict = {}

    for link in links:
        href = link.get("href", "").lower()
        text = link.text.strip()
        
        if re.search(r"/discord/", href):
            continue
        
        if text:
            games_dict[text] = href

    game_titles = list(games_dict.keys())

    if game_titles:
        for title in game_titles:
            pass
    else:
        print("No game titles found. Report this on Github.")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")

def search_games(query, game_titles):
    results = [title for title in game_titles if query.lower() in title.lower()]
    return results

search_query = input("Enter a game title to search: ")
search_results = search_games(search_query, game_titles)

if search_results:
    print("Search Results:")
    for idx, result in enumerate(search_results, start=1):
        print(f"{idx}. {result}")
    
    try:
        selection = int(input("Select a game by entering the corresponding number: "))
        if 1 <= selection <= len(search_results):
            selected_game = search_results[selection - 1]
            selected_link = games_dict[selected_game]  # Retrieve the link from the dictionary
            print(f"You selected: {selected_game}")
            print(f"Link: https://steamrip.com{selected_link}")
        else:
            print("Invalid selection.")
    except ValueError:
        print("Invalid input. Please enter a number.")
else:
    print("No matching game titles found.")
    
#scrape download links
game_url = f"https://steamrip.com{selected_link}"

keywords = ["megadb.com", "buzzheavier.com", "gofile.io"]

def scrape_buzzheavier(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)
        for link in links:
            href = link['href']
            full_dl_url = f"https:{href}" if href.startswith("//") else href
            if full_dl_url.startswith("https://buzzheavier.com/dl/"):
                print(f"Found direct download link: {full_dl_url}")
                return
        print(f"No direct download link found on {url}")
    except requests.RequestException as e:
        print(f"Failed to fetch {url}: {e}")


def scrape_links(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)
        for link in links:
            href = link['href']
            full_url = f"https:{href}" if href.startswith("//") else href
            if any(keyword in full_url for keyword in keywords):
                print(f"Found link: {full_url} on site: {url}")
                if "buzzheavier.com" in full_url:
                    scrape_buzzheavier(full_url)
    except requests.RequestException as e:
        print(f"Failed to fetch {url}: {e}")

scrape_links(game_url)
    
# url = "https://cs.rin.ru/"
# url = "https://gamesdrive.net/"
# url = "https://gog-games.to/"
# url = "https://forum.torrminatorr.com/"
# url = "https://ankergames.net/"
# url = "https://www.ovagames.com/"
# url = "https://online-fix.me/"
# url = "https://gamebounty.world/"
# url = "https://steamgg.net/"
# url = "https://g4u.to/"
# url = "https://appnetica.com/"
# url = "https://atopgames.com/"
# url = "https://games4u.org/"
# url = "https://rexagames.com/"
# url = "https://cr4ckpass.online/"
# url = "https://getfreegames.net/"
# url = "https://gload.to/"
# url = "https://steamunderground.net/"
# url = "https://worldofpcgames.com/"
# url = "http://www.leechinghell.pw/"
# url = "https://awtdg.site/"
# url = "https://www.cg-gamespc.com/"
# url = "https://gamepcfull.com/"

# Repacks/Torrents
# url = "https://www.kaoskrew.org/"
# url = "https://fitgirl-repacks.site/"
# url = "https://m4ckd0ge-repacks.site/"
# url = "https://byxatab.com/"
# url = "https://digital-zone.xyz/"
# url = "https://elamigos.site/"
# url = "https://dodi-repacks.site/"
# url = "https://www.tiny-repacks.win/"
# url = "https://freegogpcgames.com/"
# url = "https://www.magipack.games/"
# url = "https://collectionchamber.blogspot.com/"
# url = "https://archive.org/details/classicpcgames"
# url = "https://websites.umich.edu/~archive/"