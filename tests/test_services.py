from src.services import get_simple_search


def test_get_simple_search(df_for_tests):
    assert get_simple_search("ЖКХ", df_for_tests) == ('[\n'
                                                      '    {\n'
                                                      '        "Дата операции": "30.12.2021 01:00:00",\n'
                                                      '        "Дата платежа": "30.12.2021",\n'
                                                      '        "Сумма операции": 1442.11,\n'
                                                      '        "Сумма операции с округлением": 1442.11,\n'
                                                      '        "Категория": "ЖКХ",\n'
                                                      '        "Описание": "ЖКХ Услуги",\n'
                                                      '        "Номер карты": null,\n'
                                                      '        "Статус": "OK"\n'
                                                      '    }\n'
                                                      ']')
