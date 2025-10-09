from dataclasses import dataclass


@dataclass
class AppState:
    debug: bool = False
    tracker: str = "rutracker"
    api_url: str = "https://api.michijackson.xyz"


state = AppState()