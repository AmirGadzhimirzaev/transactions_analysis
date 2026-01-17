import pandas as pd
import pytest

from config import DATA_DIR


@pytest.fixture
def df_for_tests():

    return pd.read_excel(DATA_DIR)
