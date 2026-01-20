from src.services import get_simple_search


def test_get_simple_search(df_for_tests):
    my_df = df_for_tests

    assert len(get_simple_search("ЖКХ", my_df)) == 25063
    assert len(get_simple_search("Супермаркеты", my_df)) == 1202645
    assert len(get_simple_search("Переводы", my_df)) == 188676