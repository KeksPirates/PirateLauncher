from dataclasses import dataclass, asdict
from typing import List

@dataclass
class Post:
    id: int
    title: str
    url: str

@dataclass
class SearchResponse:
    success: bool
    query: str
    data: List[Post]
    count: int
    cached: bool = False

    def to_dict(self):
        d = asdict(self)
        return {
            'count': d['count'],
            'data': d['data'],
            'query': d['query'],
            'success': d['success'],
            'cached': d['cached']
        }