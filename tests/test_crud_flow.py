def test_crud_flow_for_all_entities(test_client):
    headers = {"X-API-Key": "767ge4j63d"}

    political_body = test_client.post(
        "/political-bodies",
        json={"name": "US Senate", "description": "Upper chamber"},
        headers=headers,
    )
    assert political_body.status_code == 201
    political_body_id = political_body.json()["id"]

    politician = test_client.post(
        "/politicians",
        json={
            "political_body_id": political_body_id,
            "name": "Jane Doe",
            "current_position": "Senator",
            "start_date": "2024-01-01",
            "end_date": None,
        },
        headers=headers,
    )
    assert politician.status_code == 201
    politician_id = politician.json()["id"]

    channel = test_client.post(
        "/social-channels",
        json={
            "name": "X",
            "audience_type": "Public",
            "download_type": "api",
            "download_frequency": "daily",
        },
        headers=headers,
    )
    assert channel.status_code == 201
    channel_id = channel.json()["id"]

    account = test_client.post(
        "/accounts",
        json={
            "politician_id": politician_id,
            "social_channel_id": channel_id,
            "total_audience": 10000,
        },
        headers=headers,
    )
    assert account.status_code == 201
    account_id = account.json()["id"]

    read_account = test_client.get(f"/accounts/{account_id}", headers=headers)
    assert read_account.status_code == 200
    assert read_account.json()["total_audience"] == 10000

    updated = test_client.put(
        f"/accounts/{account_id}",
        json={"total_audience": 12000},
        headers=headers,
    )
    assert updated.status_code == 200
    assert updated.json()["total_audience"] == 12000

    deleted = test_client.delete(f"/accounts/{account_id}", headers=headers)
    assert deleted.status_code == 204
