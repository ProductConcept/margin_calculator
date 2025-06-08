"""Command line utilities for the margin calculator."""

import argparse
from decimal import Decimal

from margin_calculator.calculator import cena_z_marzy, licz_marze_z_ceny


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Command line interface for margin calculations"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    marza_parser = subparsers.add_parser(
        "marza", help="Calculate margin fraction from price"
    )
    marza_parser.add_argument("tkw", type=Decimal, help="Unit production cost")
    marza_parser.add_argument("cena", type=Decimal, help="Selling price")

    cena_parser = subparsers.add_parser(
        "cena", help="Calculate price from desired margin"
    )
    cena_parser.add_argument("tkw", type=Decimal, help="Unit production cost")
    cena_parser.add_argument(
        "marza", type=Decimal, help="Desired margin expressed as a fraction"
    )

    args = parser.parse_args()

    if args.command == "marza":
        result = licz_marze_z_ceny(args.tkw, args.cena)
    else:  # "cena"
        result = cena_z_marzy(args.tkw, args.marza)

    print(result)


if __name__ == "__main__":
    main()
