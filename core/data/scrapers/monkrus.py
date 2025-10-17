from core.utils.data.state import state, Post
from bs4 import BeautifulSoup
import requests



def scrape_monkrus_telegram():
    telegram_channel = "https://t.me/s/real_monkrus/"
    posts: list[Post] = []

    response = requests.get(telegram_channel)
    print(response.status_code) # rm later

    soup = BeautifulSoup(response.text, "html.parser")
    posts = soup.find_all("div", class_=["tgme_widget_message_wrap js-widget_message_wrap", "tgme_widget_message_wrap js-widget_message_wrap date_visible"])

    for post in posts:
        posts_txt = post.find("div", class_="tgme_widget_message_text js-message_text") # this doesnt work



    print(posts_txt)



scrape_monkrus_telegram()