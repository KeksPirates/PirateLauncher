from dataclasses import dataclass
from typing import Optional, Any, List, Dict
from pathlib import Path

@dataclass
class AppState:
    posts: List[Dict[str, Any]]
    post_titles: List[str]
    post_urls: List[str]
    post_author: List[str]
    downloads: List[str]
    debug: bool = False
    tracker: str = "rutracker"
    api_url: str = "https://api.michijackson.xyz"
    download_path:  str = str(Path.home() / "Downloads")
    speed_limit: int = 0
    aria2process: Optional[Any] = None
    aria2: Any = None
    aria2p: Any = None
    aria2_threads: int = 4

state = AppState(posts=[], post_titles=[], post_urls=[], post_author=[], downloads=[], download_path="")

@dataclass
class Post:
    text: str
