def test_home_page(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert b"Check the latest news" in response.data


def test_home_page_post(test_client):
    response = test_client.post("/")
    assert response.status_code == 405
    assert b"Check the latest news" not in response.data
