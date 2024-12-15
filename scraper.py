from bs4 import BeautifulSoup
import requests
import re

<<<<<<< HEAD
url = "https://steamrip.com/games-list-page/"

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    links = soup.find_all("a")

    for link in links:
        href = link.get("href", "").lower()
        text = link.text.strip()
        
        if re.search(r"/Discord/", href):
            continue

    games = soup.find_all("li")
    if games:
        print("Games Found:")
        for game in games:
            print(game.text.strip())
    else:
        print("No game titles found. Report this on Github.")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
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

# # Repacks/Torrents
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
=======
# DirectDL
DDL = {
    "https://steamrip.com/",
    "https://cs.rin.ru/",
    "https://gamesdrive.net/",
    "https://gog-games.to/",
    "https://forum.torrminatorr.com/",
    "https://ankergames.net/",
    "https://www.ovagames.com/",
    "https://online-fix.me/",
    "https://gamebounty.world/",
    "https://steamgg.net/",
    "https://g4u.to/",
    "https://appnetica.com/",
    "https://atopgames.com/",
    "https://games4u.org/",
    "https://rexagames.com/",
    "https://cr4ckpass.online/",
    "https://getfreegames.net/",
    "https://gload.to/",
    "https://steamunderground.net/",
    "https://worldofpcgames.com/",
    "http://www.leechinghell.pw/",
    "https://awtdg.site/",
    "https://www.cg-gamespc.com/"
    "https://gamepcfull.com/",
}

# Repacks/Torrents
re_tor = {
    "https://www.kaoskrew.org/",
    "https://fitgirl-repacks.site/",
    "https://m4ckd0ge-repacks.site/",
    "https://byxatab.com/",
    "https://digital-zone.xyz/",
    "https://elamigos.site/",
    "https://dodi-repacks.site/",
    "https://www.tiny-repacks.win/",
    "https://freegogpcgames.com/",
    "https://www.magipack.games/",
    "https://collectionchamber.blogspot.com/",
    "https://archive.org/details/classicpcgames",
    "https://websites.umich.edu/~archive/",
}
>>>>>>> origin/main
