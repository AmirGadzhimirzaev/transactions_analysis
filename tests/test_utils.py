import datetime
from unittest.mock import patch

import pandas as pd
import pytest

from src.utils import get_greetings, get_filtered_df, get_card_data, get_top_trans, get_currency_rates, \
    get_stock_price

example_time_night = datetime.datetime(2020, 2, 11, 3, 0, 23)
example_time_morning = datetime.datetime(2020, 2, 11, 6, 0, 23)
example_time_afternoon = datetime.datetime(2020, 2, 11, 12, 0, 23)
example_time_evening = datetime.datetime(2020, 2, 11, 19, 0, 23)


@pytest.fixture
def df_for_tests():
    test_df = pd.DataFrame({
        "Дата операции": ["30.12.2021 01:00:00", "20.12.2021 01:00:00", "10.12.2021 01:00:00"],
        "Дата платежа": ["30.12.2021", "20.12.2021", "10.12.2021"],
        "Сумма операции": [1442.11, -23.22, -334.55],
        "Сумма операции с округлением": [1442.11, 23.22, 334.55],
        "Категория": ["ЖКХ", "Бонус", "Маркет"],
        "Описание": ["ЖКХ Услуги", "Бонус за покупку", "Яндекс Маркет"],
        "Номер карты": [None, "*2333", "*3222"],
        "Статус": ["OK", "OK", "OK"]})

    return test_df


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

    assert len(get_filtered_df("2021-12-22 01:00:00", "some.xlsx")) == 2

    mock_read_excel.assert_called_once_with("some.xlsx")


@patch("json.dumps")
def test_get_card_data(mock_json, df_for_tests):
    mock_json.return_value = '{"key": "value"}'

    assert get_card_data(df_for_tests) == '{"key": "value"}'

    mock_json.assert_called_once_with({'cards': [{'last_digits': '2333', 'total_spent': -23.22, 'cashback': -0.23},
                                                 {'last_digits': '3222', 'total_spent': -334.55, 'cashback': -3.35}]})


@patch("json.dumps")
@patch("pandas.DataFrame.nlargest")
def test_get_top_trans(mock_nlargest, mock_json, df_for_tests):
    mock_nlargest.return_value = df_for_tests.head(2)
    mock_json.return_value = '{"key": "value"}'

    assert get_top_trans(df_for_tests) == '{"key": "value"}'

    mock_nlargest.assert_called_once()
    mock_json.assert_called_once_with({'top_transactions': [
        {'date': '30.12.2021', 'amount': 1442.11, 'category': 'ЖКХ', 'description': 'ЖКХ Услуги'},
        {'date': '20.12.2021', 'amount': -23.22, 'category': 'Бонус', 'description': 'Бонус за покупку'}]},
        ensure_ascii=False)


@patch("json.dumps")
@patch("requests.models.Response.json")
def test_get_currency_rates(mock_requests_json, mock_json):
    mock_requests_json.return_value = {"conversion_rates": {"USD": 13.444, "RUB": 111.3222}}
    mock_json.return_value = '{"test": "test"}'

    assert get_currency_rates() == '{"test": "test"}'

    mock_requests_json.assert_called()
    mock_json.assert_called_once()


@patch("json.dumps")
@patch("requests.get")
def test_get_stock_price(mock_requests, mock_json):
    mock_requests.return_value.json.return_value = [{"symbol": "AAL", "price": 221}]
    mock_json.return_value = '{"test": "test"}'

    assert get_stock_price() == '{"test": "test"}'

    mock_requests.assert_called()
    mock_json.assert_called_once()
