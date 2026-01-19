import json

from src.services import get_simple_search


def test_get_simple_search(df_for_tests):
    my_df = df_for_tests

    assert get_simple_search("ЖКХ", my_df) == json.dumps(
        [{"Дата операции": "30.12.2021 01:00:00",
          "Дата платежа": "30.12.2021",
          "Сумма операции": 1442.11,
          "Сумма платежа": 100,
          "Сумма операции с округлением": 1442.11,
          "Категория": "ЖКХ",
          "Описание": "ЖКХ Услуги",
          "Номер карты": "*7197",
          "Статус": "OK"
          }],
        ensure_ascii=False,
        indent=4
    )
