def test_protected_endpoint_requires_api_key(test_client):
    response = test_client.get("/political-bodies")
    assert response.status_code == 401


def test_protected_endpoint_accepts_valid_api_key(test_client):
    response = test_client.get("/political-bodies", headers={"X-API-Key": "767ge4j63d"})
    assert response.status_code == 200
