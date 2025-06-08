"""Utility helpers for converting user input to numeric types."""

from decimal import Decimal, InvalidOperation
from typing import Optional


def _to_decimal(value: str, *, none_on_error: bool = False) -> Optional[Decimal]:
    """Convert user input to ``Decimal``.

    When ``none_on_error`` is ``True``, ``None`` is returned for invalid values.
    Empty strings and ``None`` are treated as ``Decimal('0')`` regardless of the
    flag.
    """
    if value is None or value == "":
        return Decimal("0")
    try:
        return Decimal(value.replace(",", "."))
    except (InvalidOperation, AttributeError):
        return None if none_on_error else Decimal("0")


def _to_int(value: str, *, none_on_error: bool = False) -> Optional[int]:
    """Convert user input to ``int``.

    When ``none_on_error`` is ``True``, ``None`` is returned for invalid values.
    Empty strings and ``None`` are treated as ``0`` regardless of the flag.
    """
    dec = _to_decimal(value, none_on_error=none_on_error)
    if dec is None:
        return None if none_on_error else 0
    try:
        return int(dec)
    except (InvalidOperation, ValueError):
        return None if none_on_error else 0
