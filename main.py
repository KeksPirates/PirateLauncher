from ui.clinterface import asciititle;
from core.uztracker_scraper import scrape_uztracker;
import os



def search():
    asciititle()
    searchquery = input("Enter Search Query: ")
    result = scrape_uztracker(searchquery)
    if result is None:
        clear()
        asciititle()
        print("No results found for your Query.\n")
        return
    return result

def select_result(result):
    resulttitles, resultlinks = result
    clear()
    asciititle()
    for i, title in enumerate(resulttitles, 1):
        print(f"({i}) {title}")
    selection = input("\n Enter the Number of the Program you want to download: ")


    try:
        index = int(selection) - 1
        if 0 <= index < len(resultlinks): # note for myself: py starts counting at 0; check if number is not negative, check if number is not more than list length.
            selected = "https://uztracker.net/" + resultlinks[index].lstrip("./")
            post_url = selected
            return selected
        else:
            print("Invalid Selection.")

    except ValueError:
        print(Exception)
        return

    
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')







if __name__ == "__main__":
    clear()
    results = search()
    selected = select_result(results)
    print(selected)


