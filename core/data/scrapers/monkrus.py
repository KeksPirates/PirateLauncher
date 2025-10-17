from core.utils.data.state import state, Post
from bs4 import BeautifulSoup
import requests



def scrape_monkrus_telegram():
    telegram_channel = "https://t.me/s/real_monkrus/"
    posts: list[Post] = []

    response = requests.get(telegram_channel)
    print(response.status_code) # rm later

    soup = BeautifulSoup(response.text, "html.parser")
    bubbles = soup.find_all("div", class_="tgme_widget_message_bubble")

    for bubble in bubbles:
        post_txt = bubble.find("div", class_="tgme_widget_message_text js-message_text") 

        title = post_txt.b.text
        url = bubble.find("a", href=lambda x: x and x.startswith("https://uztracker.net"))



        posts.append(Post(
            id = len(posts) + 1,
            title = title,
            url = url,
            author = "m0nkrus"
            
        ))

    print(posts)



scrape_monkrus_telegram()