from unittest .mock import patch


def test_save_news_endpoint(test_client):
    with patch('api.repository.mongo.insert_to_db') as mock:
        request_data = b'[{"title": "Test article", "url": "https://testurl"}]'
        response = test_client.post("/api/news/save", data=request_data)
        assert response.status_code == 200
        assert mock.call_count == 1


def test_save_news_endpoint_invalid(test_client):
    with patch('api.repository.mongo.insert_to_db') as mock:
        request_data = b'[{"wrong_field": "Test article", "url": "https://testurl"}]'
        expected_message = b"Input json cannot be converted to list of Article objects " \
                   b"(unexpected keyword argument \'wrong_field\'"

        response = test_client.post("/api/news/save", data=request_data)
        assert response.status_code == 400
        assert mock.call_count == 0
        assert expected_message in response.data

