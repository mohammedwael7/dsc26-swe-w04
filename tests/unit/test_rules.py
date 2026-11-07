import pytest

from nour_transfers.rules import can_transfer, days_of_cover, priority


def test_days_of_cover_divides_stock_by_daily_sales():
    assert days_of_cover(12, 3) == 4


def test_days_of_cover_returns_none_when_sales_are_zero():
    assert days_of_cover(12, 0) is None


@pytest.mark.parametrize("stock,sales", [(-1, 1), (1, -1), (-1, -1)])
def test_days_of_cover_rejects_negative_inputs(stock, sales):
    with pytest.raises(ValueError):
        days_of_cover(stock, sales)


def test_chronic_item_under_three_days_is_urgent():
    assert priority(True, 2.99) == "urgent"


def test_non_chronic_item_under_three_days_is_high_not_urgent():
    assert priority(False, 2) == "high"


def test_exactly_three_days_is_high_not_urgent():
    assert priority(True, 3) == "high"


def test_cover_under_seven_days_is_high():
    assert priority(False, 6.99) == "high"


@pytest.mark.parametrize("cover", [7, 10, None])
def test_cover_of_seven_or_more_or_indefinite_is_normal(cover):
    assert priority(True, cover) == "normal"


def test_can_transfer_when_source_keeps_exactly_reserve():
    assert can_transfer(10, 5, 5) is True


def test_can_transfer_rejects_source_dropping_below_reserve():
    assert can_transfer(9, 5, 5) is False


@pytest.mark.parametrize("quantity", [0, -1])
def test_can_transfer_rejects_nonpositive_quantity(quantity):
    assert can_transfer(20, quantity, 5) is False
