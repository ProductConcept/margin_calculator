import ast
import unittest
from decimal import Decimal
from pathlib import Path


def _load_functions():
    """Load calculation functions from app.py without running Streamlit UI."""
    tree = ast.parse(Path(__file__).resolve().parents[1].joinpath('app.py').read_text(), filename='app.py')
    namespace = {'Decimal': Decimal}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in {'licz_marze_z_ceny', 'cena_z_marzy'}:
            mod = ast.Module(body=[node], type_ignores=[])
            exec(compile(mod, filename='app.py', mode='exec'), namespace)
    return namespace['licz_marze_z_ceny'], namespace['cena_z_marzy']


licz_marze_z_ceny, cena_z_marzy = _load_functions()


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


if __name__ == '__main__':
    unittest.main()
