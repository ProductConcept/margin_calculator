import sys
import subprocess
from pathlib import Path


def test_cli_marza():
    repo_parent = Path(__file__).resolve().parents[2]
    result = subprocess.run(
        [sys.executable, '-m', 'margin_calculator.cli', 'marza', '50', '100'],
        capture_output=True,
        text=True,
        cwd=repo_parent,
    )
    assert result.returncode == 0
    assert result.stdout.strip() == '0.5'


def test_cli_cena():
    repo_parent = Path(__file__).resolve().parents[2]
    result = subprocess.run(
        [sys.executable, '-m', 'margin_calculator.cli', 'cena', '50', '0.2'],
        capture_output=True,
        text=True,
        cwd=repo_parent,
    )
    assert result.returncode == 0
    assert result.stdout.strip() == '62.5'

