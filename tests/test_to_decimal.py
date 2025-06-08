from decimal import Decimal

from utils import _to_decimal


def test_to_decimal_with_dot_and_comma():
    assert _to_decimal("10.5") == Decimal("10.5")
    assert _to_decimal("10,5") == Decimal("10.5")


def test_to_decimal_empty_and_none():
    assert _to_decimal("") == Decimal("0")
    assert _to_decimal(None) == Decimal("0")


def test_to_decimal_invalid_string():
    assert _to_decimal("abc") == Decimal("0")
    assert _to_decimal("1,000.50") == Decimal("0")


def test_to_decimal_invalid_string_none():
    assert _to_decimal("abc", none_on_error=True) is None
    assert _to_decimal("1,000.50", none_on_error=True) is None


def test_to_decimal_valid_with_flag():
    assert _to_decimal("10.5", none_on_error=True) == Decimal("10.5")
    assert _to_decimal("10,5", none_on_error=True) == Decimal("10.5")

