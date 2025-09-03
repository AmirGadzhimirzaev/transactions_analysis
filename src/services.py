import json
import logging
import re

import pandas as pd

from config import LOGS_DIR

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s: %(message)s",
    filename=LOGS_DIR["web_page_logs"],
    filemode="w",
    encoding="UTF-8",
)

reports_logger = logging.getLogger("reports_data")


def get_simple_search(user_search: str, transactions: list[dict]) -> str:
    """Функция принимает строку для поиска, возвращается JSON-ответ со всеми транзакциями,
    содержащими запрос в описании или категории."""

    df = pd.DataFrame(transactions)

    pattern = re.compile(f"{user_search}", flags=re.IGNORECASE)

    found_info = df[
        (df["Категория"].str.contains(pattern, regex=True, na=False))
        | (df["Описание"].str.contains(pattern, regex=True, na=False))
    ]

    return json.dumps(found_info.to_dict(orient="records"), ensure_ascii=False, indent=4)
