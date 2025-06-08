from utils import _to_int


def test_to_int_valid_strings():
    assert _to_int("10") == 10
    assert _to_int("10.5") == 10
    assert _to_int("10,5") == 10


def test_to_int_invalid_input():
    assert _to_int("abc") == 0
    assert _to_int("") == 0
    assert _to_int(None) == 0

