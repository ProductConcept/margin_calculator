import unittest
from decimal import Decimal

from margin_calculator.calculator import licz_marze_z_ceny, cena_z_marzy


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

    def test_example_discount_price_positive_profit(self):
        """Example with price inputs should yield positive profit after drop."""
        tkw = Decimal('80')
        cena_stara = Decimal('120')
        cena_nowa = Decimal('100')

        marza_stara = licz_marze_z_ceny(tkw, cena_stara) * 100
        marza_nowa = licz_marze_z_ceny(tkw, cena_nowa) * 100

        zysk_stary = cena_stara - tkw
        zysk_nowy = cena_nowa - tkw

        self.assertEqual(marza_stara, Decimal('33.33333333333333333333333333'))
        self.assertEqual(marza_nowa, Decimal('20'))
        self.assertGreater(zysk_nowy, Decimal('0'))


if __name__ == '__main__':
    unittest.main()
