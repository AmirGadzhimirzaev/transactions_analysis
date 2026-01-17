import json

import numpy as np

from src.services import get_simple_search


def test_get_simple_search(df_for_tests):
    my_df = df_for_tests.head(1)

    assert get_simple_search("Колхоз", my_df) == json.dumps([
        {
            "Дата операции": "31.12.2021 16:44:00",
         "Дата платежа": "31.12.2021",
         "Номер карты": "*7197",
         "Статус": "OK",
         "Сумма операции": -160.89,
         "Валюта операции": "RUB",
         "Сумма платежа": -160.89,
         "Валюта платежа": "RUB",
         "Кэшбэк": np.nan,
         "Категория": "Супермаркеты",
         "MCC": 5411.0,
         "Описание": "Колхоз",
         "Бонусы (включая кэшбэк)": 3,
         "Округление на инвесткопилку": 0,
         "Сумма операции с округлением": 160.89
        }
    ], ensure_ascii=False, indent=4)
