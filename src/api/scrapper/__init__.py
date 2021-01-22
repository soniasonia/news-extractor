from typing import List
from api.scrapper.news import Article, TvnArticle
from api.scrapper.extractors import Extractor, get_extractor

# Implement PEP 3107 -- Function Annotations

def collect_articles(url: str) -> List[Article]:
    extractor = get_extractor(url)
    return extractor.extract()

