from tests.helpers import transfer_payload


def test_same_branch_request_is_rejected_as_unprocessable(client):
    response = client.post(
        "/v1/transfers", json=transfer_payload(toBranch="branch-a")
    )
    assert response.status_code == 422


def test_below_reserve_error_uses_problem_media_type_and_type(client):
    response = client.post(
        "/v1/transfers", json=transfer_payload(quantity=26)
    )
    assert response.status_code == 409
    assert response.headers["content-type"].startswith("application/problem+json")
    assert response.json()["type"].endswith("below-reserve")


def test_request_for_unknown_item_is_not_found(client):
    response = client.post(
        "/v1/transfers", json=transfer_payload(itemCode="MISSING")
    )
    assert response.status_code == 404
    assert response.headers["content-type"].startswith("application/problem+json")


def test_transfer_response_requested_at_is_utc_with_z_suffix(client):
    response = client.post("/v1/transfers", json=transfer_payload())
    assert response.status_code in (200, 201)
    requested_at = response.json()["requestedAt"]
    assert requested_at.endswith("Z")


def test_approval_moves_stock_once_and_second_approval_is_rejected(client):
    requested = client.post("/v1/transfers", json=transfer_payload())
    assert requested.status_code in (200, 201)
    transfer_id = requested.json()["id"]

    first = client.post(f"/v1/transfers/{transfer_id}/approve")
    assert first.status_code == 200
    assert client.get("/v1/branches/branch-a/stock/MED-A").json()["quantity"] == 27
    assert client.get("/v1/branches/branch-b/stock/MED-A").json()["quantity"] == 5

    second = client.post(f"/v1/transfers/{transfer_id}/approve")
    assert second.status_code == 409
    assert second.json()["type"].endswith("not-pending")


def test_unknown_transfer_approval_is_not_found(client):
    response = client.post("/v1/transfers/no-such-transfer/approve")
    assert response.status_code == 404


def test_cors_allows_the_two_documented_origins_and_credentials(client):
    for origin in ("https://branch.nour.example", "http://localhost:5173"):
        response = client.options(
            "/v1/transfers",
            headers={
                "Origin": origin,
                "Access-Control-Request-Method": "POST",
            },
        )
        assert response.headers.get("access-control-allow-origin") == origin
        assert response.headers.get("access-control-allow-credentials") == "true"


def test_cors_does_not_allow_an_arbitrary_origin(client):
    response = client.options(
        "/v1/transfers",
        headers={
            "Origin": "https://attacker.example",
            "Access-Control-Request-Method": "POST",
        },
    )
    assert response.headers.get("access-control-allow-origin") != "https://attacker.example"


def test_inbox_orders_urgent_before_high_before_normal(client):
    # MED-A has one day of cover at the destination and is chronic (urgent).
    normal = client.post(
        "/v1/transfers",
        json=transfer_payload(itemCode="MED-B", quantity=1),
    )
    urgent = client.post("/v1/transfers", json=transfer_payload(itemCode="MED-A"))
    assert normal.status_code in (200, 201)
    assert urgent.status_code in (200, 201)
    inbox = client.get("/v1/branches/branch-b/transfers")
    assert inbox.status_code == 200
    cards = inbox.json()
    if isinstance(cards, dict):
        cards = cards.get("transfers", cards.get("items"))
    assert cards[0]["id"] == urgent.json()["id"]


def test_invalid_quantity_is_rejected(client):
    response = client.post("/v1/transfers", json=transfer_payload(quantity=0))
    assert response.status_code == 422
