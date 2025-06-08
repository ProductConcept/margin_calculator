from decimal import Decimal, InvalidOperation


def _to_decimal(value: str) -> Decimal:
    """Convert user input to ``Decimal``. Returns ``Decimal('0')`` on error."""
    if value is None or value == "":
        return Decimal("0")
    try:
        return Decimal(value.replace(",", "."))
    except (InvalidOperation, AttributeError):
        return Decimal("0")


def _to_int(value: str) -> int:
    """Convert user input to ``int``. Returns ``0`` on error."""
    try:
        return int(_to_decimal(value))
    except (InvalidOperation, ValueError):
        return 0
