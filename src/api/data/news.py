from abc import ABC
from dataclasses import dataclass

@dataclass
class Article(ABC):
    title: str
    url: str

@dataclass
class TvnArticle(Article):
    pass