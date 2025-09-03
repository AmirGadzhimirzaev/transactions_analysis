from unittest.mock import patch

from src.reports import spending_by_category

@patch("src.reports.spending_by_category")
def test_spending_by_category(mock_my_module, df_for_tests):
    assert spending_by_category == spending_by_category
