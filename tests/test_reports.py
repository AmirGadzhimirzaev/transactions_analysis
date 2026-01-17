from unittest.mock import patch

import pandas as pd

from config import DATA_DIR
from src.reports import spending_by_category


def test_spending_by_category():
    assert spending_by_category(pd.read_excel(DATA_DIR), "ЖКХ", "2021-12-22 01:00:00") == ""
