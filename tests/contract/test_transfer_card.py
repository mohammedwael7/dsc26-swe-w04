import json
from pathlib import Path

from jsonschema import validate

from tests.helpers import transfer_payload


def test_transfer_card_matches_schema_and_uses_utc_timestamp(client):
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
