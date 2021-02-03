from typing import List
from api.data.news import Article
from api.scrapper.extractors import get_extractor


def collect_articles(url: str) -> List[Article]:
    extractor = get_extractor(url)
    return extractor.extract()
