from unittest.mock import patch

from src.views import get_main_json_answer


@patch("json.dumps")
def test_get_main_json_answer(mock_json):
    mock_json.return_value = '{"test": "test"}'

    assert get_main_json_answer("2021-12-22 01:00:00") == '{"test": "test"}'

    mock_json.assert_called()