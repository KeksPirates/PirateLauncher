from dataclasses import dataclass, asdict
from typing import List

@dataclass
class Post:
    id: int
    title: str
    url: str
    author: str

@dataclass
class SearchResponse:
    success: bool
    query: str
    data: List[Post]
    count: int
    cached: bool = False

    def to_dict(self):
        return asdict(self)