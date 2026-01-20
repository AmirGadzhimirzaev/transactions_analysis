import pytest

from src.reports import spending_by_category


@pytest.mark.parametrize('test_category, test_date, expected',
                         [
                             ("ЖКХ", "2021-11-15 01:00:00", 8),
                             ("Супермаркеты", "2020-10-15 01:00:00", 147),
                             ("Переводы", "2022-01-15 01:00:00", 25),
                          ])
def test_spending_by_category(df_for_tests, test_category, test_date, expected):
    result = spending_by_category(df_for_tests, test_category, test_date)

    assert len(result) == expected
