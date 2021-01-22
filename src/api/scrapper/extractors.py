from urllib.request import urlopen
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod, abstractproperty
from typing import List
from api.scrapper.news import Article, TvnArticle

# Implement PEP 3107 -- Function Annotations

class Extractor(ABC):
    @property
    @abstractmethod
    def url(self) -> str:
        pass

    @abstractmethod
    def extract(self) -> List[Article]:
        pass


class TvnExtractor(Extractor):
    url = "https://tvn24.pl/"
    def extract(self) -> List[TvnArticle]:
        with urlopen(self.url) as response:
            soup = BeautifulSoup(response.read(), "html.parser")

        result = soup.select(".news-of-the-day>ul>li>div>div")
        articles = [TvnArticle(title=div.get_text(), url=div.a['href'])
                    for div in result]

        result = soup.select(".virtual-page>div.teaser-wrapper>article>div>div")
        more_articles = [TvnArticle(
            title=div.select("h2")[0].get_text()
            if len(div.select("h2")) > 0 else "",
            url=div.a['href'])
            for div in result]

        articles.extend(more_articles)
        return articles

EXTRACTORS = {TvnExtractor}

def get_extractor(url: str) -> Extractor:
    for ex in EXTRACTORS:
        if ex.url == url:
            return ex()
    raise Exception(f"Scrapper for {url} not implemented")
