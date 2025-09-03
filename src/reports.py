import json
import logging
from datetime import datetime
from functools import wraps

import pandas as pd

from config import REPORT_DIR, LOGS_DIR

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s: %(message)s",
    filename=LOGS_DIR["web_page_logs"],
    filemode="w",
    encoding="UTF-8",
)

reports_logger = logging.getLogger("reports_data")


def save_to_file(path_to_file: str = REPORT_DIR):
    """Декоратор для записи отчета в файл .json"""
    reports_logger.info("Декоратор 'save_to_file' задействован")

    def save_to_file_default(func):
        @wraps(func)
        def inner(*args, **kwargs):
            with open(path_to_file, "w", encoding="utf-8") as f:
                json.dump((func(*args, **kwargs).to_dict(orient="records")), f, ensure_ascii=False, indent=4)

            return func(*args, **kwargs)

        return inner

    return save_to_file_default


@save_to_file()
def spending_by_category(df: pd.DataFrame,
                         category: str,
                         date: str | None) -> pd.DataFrame:
    """Функция возвращает траты по заданной категории за последние три месяца (от переданной даты)"""

    reports_logger.info("Вызвана функция 'spending_by_category'")

    if isinstance(date, str):
        data_as_dt = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    else:
        data_as_dt = datetime.now()

    start_date = data_as_dt - pd.DateOffset(months=3)
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = data_as_dt.strftime("%Y-%m-%d")
    date_range = pd.date_range(start_date_str, end_date_str)

    answer = df[(pd.to_datetime(df["Дата операции"], dayfirst=True).dt.normalize().isin(date_range)) & (
            df["Категория"] == category)]

    return answer
