import json

from config import DATA_DIR
from src.utils import (
    get_card_data,
    get_currency_rates,
    get_datetime,
    get_filtered_df,
    get_greetings,
    get_stock_price,
    get_top_trans,
)


def get_main_json_answer(user_time: str, path_to_excel: str = DATA_DIR) -> str:
    """Функция принимает строку с датой в формате YYYY-MM-DD HH:MM:SS и возвращает JSON-ответ
    в диапазоне от начала месяца, на который выпадает входящая дата, по входящую дату:
    1. Приветствие в зависимости от текущего времени
    2. По каждой карте: последние 4 цифры, общая сумма расходов кешбэк (1 рубль на каждые 100 рублей)
    3. Топ-5 транзакций по сумме платежа
    4. Курс волют
    5. Стоимость акций из S&P500"""

    user_time_dt = get_datetime(user_time)
    filtered_df = get_filtered_df(user_time_dt, path_to_excel)

    final_dict = {}

    list_of_data = [
        get_greetings(user_time_dt[0]),
        get_card_data(filtered_df),
        get_top_trans(filtered_df),
        get_currency_rates(),
        get_stock_price(),
    ]

    for data in list_of_data:
        final_dict.update(json.loads(data))

    return json.dumps(final_dict, indent=4, ensure_ascii=False)
