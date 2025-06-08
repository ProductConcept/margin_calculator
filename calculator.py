from decimal import Decimal


def licz_marze_z_ceny(tkw: Decimal, cena: Decimal) -> Decimal:
    """Return the margin as a fraction of ``cena``.

    Parameters
    ----------
    tkw : Decimal
        Unit production cost.
    cena : Decimal
        Selling price per unit.

    Returns
    -------
    Decimal
        Margin expressed as ``(cena - tkw) / cena``. ``Decimal('0')`` is
        returned when ``cena`` equals ``0``.

    Examples
    --------
    >>> licz_marze_z_ceny(Decimal('50'), Decimal('100'))
    Decimal('0.5')
    """
    return (cena - tkw) / cena if cena else Decimal("0")


def cena_z_marzy(tkw: Decimal, marza: Decimal) -> Decimal:
    """Return the sale price required to achieve ``marza``.

    Parameters
    ----------
    tkw : Decimal
        Unit production cost.
    marza : Decimal
        Desired margin expressed as a fraction (``0.25`` means ``25%``).

    Returns
    -------
    Decimal
        Price that yields ``marza`` margin. ``Decimal('0')`` is returned for
        margins greater than or equal to ``1``.

    Examples
    --------
    >>> cena_z_marzy(Decimal('50'), Decimal('0.2'))
    Decimal('62.5')
    """
    return tkw / (Decimal("1") - marza) if marza < Decimal("1") else Decimal("0")
