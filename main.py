import core.gui as gui
from core.uztracker_scraper import scrape_uztracker, get_post_title, get_magnet_link
from core.gui import run_gui











post_url = scrape_uztracker()
if post_url:
    maintitle = get_post_title(post_url)
    magnetlink = get_magnet_link(post_url)
    print(maintitle)
    print(magnetlink)



