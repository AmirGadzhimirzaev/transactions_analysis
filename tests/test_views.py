from unittest.mock import patch
import json
from src.views import get_main_json_answer

@patch("src.utils.get_currency_rates")
def test_get_main_json_answer(mock_cur, df_for_tests):
    mock_cur.return_value = ""
    my_df = df_for_tests.head(1)

    assert get_main_json_answer("2021-12-22 01:00:00", my_df) == json.dumps({"test": "test"}, ensure_ascii=False)
