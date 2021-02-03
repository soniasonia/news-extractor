from unittest.mock import patch
from api.data.news import Article


def test_news_endpoint_url(test_client):
    with patch('api.views.main.collect_articles') as func:
        func.return_value = [Article(title="Test", url="https://test1.pl")]
        response = test_client.get("/api/news?url=123")
        assert response.status_code == 200
        assert b"Articles extracted" in response.data
        assert b"https://test1.pl" in response.data

def test_news_endpoint_no_url(test_client):
    response = test_client.get("/api/news")
    assert response.status_code == 200
    assert b"Please provide url" in response.data

def test_news_endpoint_url_not_implemented(test_client):
    response = test_client.get("/api/news?url=wrongurl")
    assert response.status_code == 200
    assert b"not implemented" in response.data
