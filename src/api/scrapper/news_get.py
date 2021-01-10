from urllib.request import urlopen
from bs4 import BeautifulSoup


def standarize_output(func):
    def wrap(*args, **kwargs):
        articles = func(*args, **kwargs)
        standard_articles = []
        for a in articles:
            standard_articles.append(
                {"title": a.get("title", ""),
                 "url": a.get("url", ""),
                 "photo": a.get("photo", "")}
            )
        return standard_articles
    return wrap


@standarize_output
def extract_tvn24(url):
    with urlopen(url) as response:
        soup = BeautifulSoup(response.read(), "html.parser")

    result = soup.select(".news-of-the-day>ul>li>div>div")
    articles = [{"title": div.get_text(), "url": div.a['href']}
                for div in result]

    result = soup.select(".virtual-page>div.teaser-wrapper>article>div>div")
    more_articles = [{
        "title": div.select("h2")[0].get_text()
        if len(div.select("h2")) > 0 else "",
        "url": div.a['href']}
        for div in result]

    articles.extend(more_articles)
    return articles


ALLOWED_URLS = {"https://tvn24.pl/": extract_tvn24}


def extract(url):
    if url in ALLOWED_URLS.keys():
        func = ALLOWED_URLS[url]
        return func(url)
    return f"{url} not implemented"
