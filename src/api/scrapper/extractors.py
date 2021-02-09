import os
from urllib.request import urlopen
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
from typing import List
from api.data.news import Article, TvnArticle


class Extractor(ABC):
    @property
    @abstractmethod
    def url(self) -> str:
        pass

    @abstractmethod
    def extract(self) -> List[Article]:
        pass

    def parse_page(self) -> BeautifulSoup:
        with urlopen(self.url) as response:
            return BeautifulSoup(response.read(), "html.parser")


class TvnExtractor(Extractor):
    url = "https://tvn24.pl/"

    def extract(self) -> List[TvnArticle]:
        soup = self.parse_page()
        articles = []

        css_selector = ".news-of-the-day>ul>li>div>div"
        result = soup.select(css_selector)
        for div in result:
            title = div.get_text()
            url = div.a['href']
            articles.append(TvnArticle(title=title, url=url))

        css_selector = ".virtual-page>div.teaser-wrapper>article>div>div"
        result = soup.select(css_selector)
        for div in result:
            if len(div.select("h2")) > 0:
                title = div.select("h2")[0].get_text()
                url = div.a['href']
                articles.append(TvnArticle(title=title, url=url))

        return articles


class FakeExtractor(Extractor):
    url = "fake"

    def extract(self) -> List[Article]:
        articles = []
        for i in range(10):
            title = 'Fake {:.>10}'.format(i)
            url = 'https://someurl{}.test'.format(i)
            articles.append(Article(title=title, url=url))

        return articles


EXTRACTORS = {TvnExtractor}
if os.environ.get != "prod":
    EXTRACTORS.add(FakeExtractor)


def get_extractor(url: str) -> Extractor:
    for ex in EXTRACTORS:
        if ex.url == url:
            return ex()
    raise NotImplementedError
