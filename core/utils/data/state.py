from dataclasses import dataclass
from typing import Optional, Any, List, Dict

@dataclass
class AppState:
    posts: List[Dict[str, Any]]
    post_titles: List[str]
    post_urls: List[str]
    debug: bool = False
    tracker: str = "rutracker"
    api_url: str = "https://api.michijackson.xyz"
    aria2process: Optional[Any] = None
    aria2_threads: int = 4

state = AppState(posts=[], post_titles=[], post_urls=[])