from bs4 import BeautifulSoup
import requests



def scrape_monkrus_telegram():
    telegram_channel = "https://t.me/s/real_monkrus/rss"

    response = requests.get(telegram_channel)
    print(response.status_code) # rm later

    soup = BeautifulSoup(response.text, 'html.parser')
    posts_txt = soup.find_all('div', class_=["tgme_widget_message_wrap js-widget_message_wrap", "tgme_widget_message_wrap js-widget_message_wrap date_visible"])

    print(posts_txt)


scrape_monkrus_telegram()