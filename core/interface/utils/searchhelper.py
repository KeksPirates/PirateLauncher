import asyncio
from core.data.scrapers.uztracker import scrape_uztracker
from core.data.scrapers.rutracker import scrape_rutracker
from core.utils.network.jsonhandler import split_data, format_data
from core.utils.data.state import state

def return_pressed(self):
        search_text = self.searchbar.text()
        if search_text == "":
            if state.debug:
                print("Error: Can't search for nothing")
            return
        if state.debug:
            print("User searched for:", search_text)
        if state.tracker == "uztracker":
            response = asyncio.run(scrape_uztracker(search_text))
        if state.tracker == "rutracker":
            response = scrape_rutracker(search_text)
        if response:
            if state.tracker == "uztracker":
                state.post_titles, state.post_urls, = response
                self.softwareList.clear()
                if state.post_titles:
                    self.softwareList.addItems(state.post_titles)
                    self.post_author_list.addItems(state.post_author)
            if state.tracker == "rutracker":
                _, state.posts, _, _, cached = split_data(response)
                state.post_titles, _, state.post_author = format_data(state.posts)
                self.post_author_list.clear()
                self.post_author_list.addItems(state.post_author)
                self.softwareList.clear()
                self.softwareList.addItems(state.post_titles)
                if state.debug == True:
                    print(f"Cached: {cached}")
        if not response:
            if state.debug:
                print(f"No Results found for \"{search_text}\"")
            self.softwareList.clear()
            self.softwareList.addItem("No Results") # replace with no results text in center