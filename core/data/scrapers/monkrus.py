from bs4 import BeautifulSoup
import requests



def scrape_monkrus_telegram(query):
    telegram_channel = "https://t.me/s/real_monkrus/"
    posts: list[dict] = []

    response = requests.get(telegram_channel)
    soup = BeautifulSoup(response.text, "html.parser")
    bubbles = soup.find_all("div", class_="tgme_widget_message_bubble")

    for bubble in bubbles:
        post_txt = bubble.find("div", class_="tgme_widget_message_text js-message_text") 

        title = post_txt.b.text
        url = bubble.find("a", href=lambda x: x and x.startswith("https://uztracker.net"))

        if query.lower() in title.lower():
            posts.append(dict(
                author = "m0nkrus",
                id = len(posts) + 1,
                title = title,
                url = url["href"]
            ))

    posts.reverse() # reverse to show most recent posts (bubbles) at top of list
    return(posts)