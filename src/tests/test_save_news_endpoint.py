from unittest .mock import patch


def test_save_news_endpoint(test_client):
    with patch('api.repository.mongo._insert_to_db') as mock:
        request_data = b'[{"title": "Test article", "url": "https://testurl"}]'
        response = test_client.post("/api/news/save", data=request_data)
        assert response.status_code == 200
        assert mock.call_count == 1


def test_save_news_endpoint_invalid_argument(test_client):
    with patch('api.repository.mongo._insert_to_db') as mock:
        request_data = b'[{"wrong_field": "Test article", ' \
                       b'"url": "https://testurl"}]'
        expected_msg = b"Input json cannot be converted to list of Article " \
                       b"objects (unexpected keyword argument \'wrong_field\'"

        response = test_client.post("/api/news/save", data=request_data)
        assert response.status_code == 400
        assert mock.call_count == 0
        assert expected_msg in response.data


def test_save_news_endpoint_missing_argument(test_client):
    with patch('api.repository.mongo._insert_to_db') as mock:
        request_data = b'[{"wrong_field": "Test article", ' \
                       b'"url": "https://testurl"}]'
        expected_msg = b"Input json cannot be converted to list of Article " \
                       b"objects (unexpected keyword argument \'wrong_field\'"

        response = test_client.post("/api/news/save", data=request_data)
        assert response.status_code == 400
        assert mock.call_count == 0
        assert expected_msg in response.data
