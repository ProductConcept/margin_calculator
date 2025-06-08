import unittest
from decimal import Decimal
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from calculator import licz_marze_z_ceny, cena_z_marzy


class TestMarginFunctions(unittest.TestCase):
    def test_licz_marze_basic(self):
        self.assertEqual(
            licz_marze_z_ceny(Decimal('50'), Decimal('100')),
            Decimal('0.5')
        )

    def test_licz_marze_zero_price(self):
        self.assertEqual(
            licz_marze_z_ceny(Decimal('50'), Decimal('0')),
            Decimal('0')
        )

    def test_licz_marze_negative(self):
        self.assertEqual(
            licz_marze_z_ceny(Decimal('80'), Decimal('60')),
            Decimal('-0.3333333333333333333333333333')
        )

    def test_licz_marze_zero_margin(self):
        self.assertEqual(
            licz_marze_z_ceny(Decimal('50'), Decimal('50')),
            Decimal('0')
        )

    def test_cena_z_marzy_basic(self):
        self.assertEqual(
            cena_z_marzy(Decimal('50'), Decimal('0.2')),
            Decimal('62.5')
        )

    def test_cena_z_marzy_over_one(self):
        self.assertEqual(
            cena_z_marzy(Decimal('10'), Decimal('1')),
            Decimal('0')
        )

    def test_cena_z_marzy_zero_margin(self):
        self.assertEqual(
            cena_z_marzy(Decimal('10'), Decimal('0')),
            Decimal('10')
        )

    def test_total_loss_quantized(self):
        tkw = Decimal('80')
        marza_stara = Decimal('0.4')
        marza_nowa = Decimal('0.2')
        qty = 100
        cena_stara = cena_z_marzy(tkw, marza_stara).quantize(Decimal('0.01'))
        cena_nowa = cena_z_marzy(tkw, marza_nowa).quantize(Decimal('0.01'))
        zysk_stary = cena_stara - tkw
        zysk_nowy = cena_nowa - tkw
        strata = (zysk_stary - zysk_nowy) * qty
        self.assertEqual(strata, Decimal('3333'))


if __name__ == '__main__':
    unittest.main()
