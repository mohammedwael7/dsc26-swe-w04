import json
from pathlib import Path

from jsonschema import validate

from tests.helpers import transfer_payload


def test_destination_inbox_transfer_card_matches_schema_and_uses_utc_timestamp(client):
    schema_path = (
        Path(__file__).resolve().parents[2]
        / "contracts"
        / "transfer_card.schema.json"
    )
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    requested = client.post("/v1/transfers", json=transfer_payload())
    assert requested.status_code in (200, 201)
    transfer_id = requested.json()["id"]
    inbox_response = client.get("/v1/branches/branch-b/transfers")
    assert inbox_response.status_code == 200
    cards = inbox_response.json()
    if isinstance(cards, dict):
        cards = cards.get("transfers", cards.get("items"))
    card = next(card for card in cards if card["id"] == transfer_id)
    validate(instance=card, schema=schema)
    assert card["requestedAt"].endswith("Z")
