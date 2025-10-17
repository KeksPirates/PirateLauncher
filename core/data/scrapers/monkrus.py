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
        post_txt = bubble.find("div", class_="tgme_widget_message_text js-message_text") # this doesnt work
        if post_txt.b:
            posts.append(Post(text=post_txt.get_text()))


    print(post_txt.b.text)



scrape_monkrus_telegram()