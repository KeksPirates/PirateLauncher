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
        response = scrape_uztracker(search_text)
        if response:
            state.post_titles, state.post_urls = response
            self.softwareList.clear()
            if state.post_titles and len(state.post_titles) > 0:
                self.softwareList.addItems(state.post_titles)
                self.show_empty_results(False)
                self.post_author_list.clear()
            else:
                if state.debug:
                    print(f"No Results for {search_text}")
                self.softwareList.clear()
                self.show_empty_results(True)
        else:
            if state.debug:
                print(f"No response from uztracker")
            self.softwareList.clear()
            self.show_empty_results(True)
    
    elif state.tracker == "rutracker":
        response = scrape_rutracker(search_text)
        if response:
            _, state.posts, _, _, cached = split_data(response)
            if state.posts == []:
                if state.debug:
                    print(f"No Results for {search_text}")
                self.softwareList.clear()
                self.show_empty_results(True)
            else:
                state.post_titles, _, state.post_author = format_data(state.posts)
                self.show_empty_results(False)
                self.post_author_list.clear()
                self.post_author_list.addItems(state.post_author)
                self.softwareList.clear()
                self.softwareList.addItems(state.post_titles)
                if state.debug == True:
                    print(f"Response Cached: {cached}")
        else:
            if state.debug:
                print(f"No response from rutracker")
            self.softwareList.clear()
            self.show_empty_results(True)