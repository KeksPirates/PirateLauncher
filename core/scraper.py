from bs4 import BeautifulSoup
import requests
import re

badphrases = {
    "About", "Request Games", "Privacy Policy", "Terms & Conditions",
    "Contact Us", "Reddit", "Back to top button", "Close", "Menu",
    "Games List", "Search for", "Home", "Categories", "Action",
    "Adventure", "Anime", "Horror", "Indie", "Multiplayer",
    "Open World", "Racing", "Shooters", "Simulation", "Sports",
    "Strategy", "Virtual Reality", "Top Games", "Recent Updates",
    "FAQ", "FAQs", "All FAQs", "How to Run Games", "Discord", "Switch skin",
    "All", "0-9", "�"
}
badphrases.update({chr(i) for i in range(ord('A'), ord('Z') + 1)})

steamrip_url = "https://steamrip.com/games-list-page/"
gog_games_url = "https://gog-games.to/api/web/all-games"

def fetch_steamrip_games(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all("a")
        games_dict = {}
        for link in links:
            href = link.get("href", "").lower()
            text = link.text.strip()
            if text:
                games_dict[text] = href
        return games_dict
    else:
        print(f"Failed to retrieve the Steamrip page. Status code: {response.status_code}")
        return {}

def fetch_gog_games(url):
    response = requests.get(url)
    if response.status_code == 200:
        games = response.json()
        games_dict = {game['title']: game['slug'] for game in games}
        return games_dict
    else:
        print(f"Failed to retrieve the GOG Games API. Status code: {response.status_code}")
        return {}

def clean_game_titles(game_titles, badphrases):
    for phrase in badphrases:
        game_titles = [re.sub(rf"\b{re.escape(phrase)}\b", "", title, flags=re.IGNORECASE).strip() for title in game_titles]
    return [re.sub(r'\s+', ' ', title).strip() for title in game_titles if title.strip()]

def search_games(query, game_titles):
    return [title for title in game_titles if query.lower() in title.lower()]

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
                return full_dl_url
        print(f"No direct download link found on {url}")
    except requests.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
    return None

def scrape_links(url, keywords):
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
                    direct_dl_link = scrape_buzzheavier(full_url)
                    if direct_dl_link:
                        print(f"Direct download link: {direct_dl_link}")
                        return
    except requests.RequestException as e:
        print(f"Failed to fetch {url}: {e}")

steamrip_games = fetch_steamrip_games(steamrip_url)
gog_games = fetch_gog_games(gog_games_url)

games_dict = {**steamrip_games, **gog_games}
game_titles = clean_game_titles(list(games_dict.keys()), badphrases)

if game_titles:
    for title in game_titles:
        pass
else:
    print("No game titles found. Please report this on Github.")

def search():
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
                selected_link = games_dict[selected_game]
            
                if selected_game in gog_games:
                    game_url = f"https://gog-games.to/game/{selected_link}"
                else:
                    game_url = f"https://steamrip.com{selected_link}"
            
                print(f"You selected: {selected_game}")
                print(f"Link: {game_url}")

                keywords = ["megadb.com", "buzzheavier.com", "gofile.io"]
                scrape_links(game_url, keywords)
        except ValueError:
            print("Invalid selection.")
    else:
        print("No results found.")
        search()
search()