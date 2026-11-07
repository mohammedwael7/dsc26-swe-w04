import json
from pathlib import Path

from jsonschema import validate

from tests.helpers import transfer_payload


def test_contract_transfer_card_matches_json_schema_and_uses_utc_timestamp(client):
    schema_path = (
        Path(__file__).resolve().parents[2]
        / "contracts"
        / "transfer_card.schema.json"
    )
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    requested = client.post("/v1/transfers", json=transfer_payload())
    assert requested.status_code in (200, 201)
    card = requested.json()
    validate(instance=card, schema=schema)
    assert "requestedAt" in card
    assert card["requestedAt"].endswith("Z")


def test_inbox_transfer_card_matches_contract_schema(client):
    schema_path = (
        Path(__file__).resolve().parents[2]
        / "contracts"
        / "transfer_card.schema.json"
    )
    schema = json.loads(schema_path.read_text(encoding="utf-8"))

    requested = client.post("/v1/transfers", json=transfer_payload())
    assert requested.status_code in (200, 201)

    inbox = client.get("/v1/branches/branch-b/transfers")
    assert inbox.status_code == 200
    cards = inbox.json()
    if isinstance(cards, dict):
        cards = cards.get("transfers", cards.get("items"))
    assert cards
    validate(instance=cards[0], schema=schema)
