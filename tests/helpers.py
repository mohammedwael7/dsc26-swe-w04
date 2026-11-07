def transfer_payload(**overrides):
    payload = {
        "fromBranch": "branch-a",
        "toBranch": "branch-b",
        "itemCode": "MED-A",
        "quantity": 3,
    }
    payload.update(overrides)
    return payload
