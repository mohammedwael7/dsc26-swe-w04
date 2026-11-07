from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient

from nour_transfers.app import create_app


@pytest.fixture
def scenario():
    """Small deterministic data set shared by API and contract tests."""
    stock = {
        "branch-a": {"MED-A": 30, "MED-B": 8},
        "branch-b": {"MED-A": 2, "MED-B": 20},
    }
    items = {
        "MED-A": {"reserve": 5, "is_chronic": True},
        "MED-B": {"reserve": 2, "is_chronic": False},
    }
    sales = {
        "branch-a": {"MED-A": 2, "MED-B": 2},
        "branch-b": {"MED-A": 1, "MED-B": 2},
    }
    return stock, items, sales


@pytest.fixture
def client(scenario):
    stock, items, sales = scenario
    app = create_app(
        stock=stock,
        items=items,
        sales=sales,
        now=datetime(2026, 11, 5, 17, 0, tzinfo=timezone.utc),
    )
    with TestClient(app) as test_client:
        yield test_client


