from core.utils.data.state import state
from core.utils.data.tracker import get_item_index
from core.utils.wrappers import run_thread
import threading


def download_selected(item, ):
    if item is not None:
        if state.debug:
            print(f"network {item.text()}")
        run_thread(threading.Thread(target=get_item_index, args=(item.text(), self.postnames, self.postlinks, state.debug)))
    else:
        if state.debug:
            print("No item selected for download.")



