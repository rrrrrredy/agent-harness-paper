from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src import app


def test_value_is_updated():
    assert app.VALUE == 2
