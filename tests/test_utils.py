import datetime
import json
from unittest.mock import patch

import pytest

from src.utils import get_card_data, get_currency_rates, get_filtered_df, get_greetings, get_stock_price, get_top_trans

example_time_night = datetime.datetime(2020, 2, 11, 3, 0, 23)
example_time_morning = datetime.datetime(2020, 2, 11, 6, 0, 23)
example_time_afternoon = datetime.datetime(2020, 2, 11, 12, 0, 23)
example_time_evening = datetime.datetime(2020, 2, 11, 19, 0, 23)


@pytest.mark.parametrize("hour, expected", [(example_time_night, '{"greeting": "Доброй ночи"}'),
                                            (example_time_morning, '{"greeting": "Доброе утро"}'),
                                            (example_time_afternoon, '{"greeting": "Добрый день"}'),
                                            (example_time_evening, '{"greeting": "Добрый вечер"}'),
                                            (None, "Неверный формат времени"),
                                            ((), "Неверный формат времени")
                                            ])
def test_greetings(hour, expected):
    assert get_greetings(hour) == expected


@patch("pandas.read_excel")
def test_get_filtered_df(mock_read_excel, df_for_tests):
    mock_read_excel.return_value = df_for_tests

    assert len(get_filtered_df("2021-12-22 01:00:00", "some.xlsx")) == 127

    mock_read_excel.assert_called_once_with("some.xlsx")


def test_get_card_data(df_for_tests):
    my_df = df_for_tests.head(1)

    assert get_card_data(my_df) == json.dumps(
        {"cards": [{"last_digits": "7197", "total_spent": -160.89, "cashback": -1.61}]})


@patch("pandas.DataFrame.nlargest")
def test_get_top_trans(mock_nlargest, df_for_tests):
    mock_nlargest.return_value = df_for_tests.head(1)

    assert get_top_trans(df_for_tests) == json.dumps(
        {"top_transactions": [{"date": "31.12.2021", "amount": -160.89, "category":
            "Супермаркеты", "description": "Колхоз"}]}, ensure_ascii=False)

    mock_nlargest.assert_called_once()


@patch("requests.get")
def test_get_currency_rates(mock_get):
    mock_get.return_value.json.return_value = {"conversion_rates": {"USD": 13.444, "RUB": 111.3222}}

    assert get_currency_rates() == json.dumps(
        {"currency_rates": [{"currency": "USD", "rate": 111.32}, {"currency": "EUR", "rate": 111.32}]})

    mock_get.assert_called()


@patch("requests.get")
def test_get_stock_price(mock_requests):
    mock_requests.return_value.json.return_value = [{"symbol": "AAL", "price": 221}]

    assert get_stock_price() == json.dumps({"stock_prices": [{"stock": "AAL", "price": 221}]})

    mock_requests.assert_called()
