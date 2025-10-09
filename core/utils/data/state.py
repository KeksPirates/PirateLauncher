from dataclasses import dataclass
from typing import Optional, Any


@dataclass
class AppState:
    debug: bool = False
    tracker: str = "rutracker"
    api_url: str = "https://api.michijackson.xyz"
    aria2process: Optional[Any] = None
    aria2_threads: int = 4


state = AppState()