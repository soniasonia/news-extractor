from typing import List
from api.data.news import Article
from api.scrapper.extractors import Extractor, get_extractor

# Implement PEP 3107 -- Function Annotations

def collect_articles(url: str) -> List[Article]:
    extractor = get_extractor(url)
    return extractor.extract()

