import logging
from pathlib import Path
import sys

# Allow importing from repo root
sys.path.append(str(Path(__file__).resolve().parents[1]))
# Silence Streamlit warnings when importing app
logging.getLogger("streamlit").setLevel(logging.CRITICAL)

from app import _to_int


def test_to_int_valid_strings():
    assert _to_int("10") == 10
    assert _to_int("10.5") == 10
    assert _to_int("10,5") == 10


def test_to_int_invalid_input():
    assert _to_int("abc") == 0
    assert _to_int("") == 0
    assert _to_int(None) == 0

