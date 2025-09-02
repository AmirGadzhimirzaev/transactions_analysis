import datetime
import json
import logging
import os

import pandas as pd
import requests
from dotenv import load_dotenv
from pandas import DataFrame

from config import ENV_DIR, LOGS_DIR, USER_SETTINGS_DIR

load_dotenv(ENV_DIR)

API_KEY_CURRENCY = os.getenv("EXCHANGE_RATE_API_KEY")
API_KEY_STOCK = os.getenv("STOCK_API_KEY")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s: %(message)s",
    filename=LOGS_DIR["web_page_logs"],
    filemode="w",
    encoding="UTF-8",
)

logger = logging.getLogger("web_page_data")


def get_greetings(user_time: datetime.datetime = datetime.datetime.now()) -> str:
    """Функция реализует приветствие"""

    logger.info("Вызвана функция 'get_greetings'")

    if not isinstance(user_time, datetime.datetime):
        return "Неверный формат времени"

    dict_of_greetings = {
        "Доброй ночи": range(5),
        "Доброе утро": range(5, 12),
        "Добрый день": range(12, 18),
        "Добрый вечер": range(18, 24),
    }

    for greeting, time_range in dict_of_greetings.items():
        if pd.to_datetime(user_time).hour in time_range:
            return json.dumps({"greeting": greeting}, ensure_ascii=False)

    return "Что-то пошло не так!"


def get_filtered_df(user_time: str, xlsx_file: str) -> DataFrame | None:
    """Функция принимает путь к файлу. Возвращает объект DataFrame в заданном диапазоне"""

    logger.info("Вызвана функция 'get_filtered_by_date'")

    try:
        df = pd.read_excel(xlsx_file)
        end_time = datetime.datetime.strptime(user_time, "%Y-%m-%d %H:%M:%S")
        date_range = pd.date_range(f"{end_time.year}-{end_time.month}", end_time)
    except Exception as e:
        logger.error(f"Ошибка в get_filtered_by_date - {e}", exc_info=True)
        return None
    else:
        return df[
            (pd.to_datetime(df["Дата операции"], dayfirst=True).dt.normalize().isin(date_range))
            & (df["Статус"] == "OK")
        ]


def get_card_data(dframe: DataFrame | None) -> str:
    """2. Функция реализует данные по карте"""

    logger.info("Вызвана функция 'get_card_data'")

    if dframe is None:
        return "Что то не так!"

    list_of_cards = []

    last_four_digits = list(dframe["Номер карты"].dropna().value_counts().keys())

    for digits in last_four_digits:
        total_spent = float(dframe["Сумма операции"].loc[dframe["Номер карты"] == digits].sum())

        json_answer = {
            "last_digits": f"{digits[1:]}",
            "total_spent": round(total_spent, 2),
            "cashback": round(total_spent / 100, 2),
        }

        list_of_cards.append(json_answer)

    cards = {"cards": list_of_cards}

    return json.dumps(cards)


def get_top_trans(dframe: DataFrame | None) -> str:
    """Функция принимает на вход дату и путь к файлу транзакций xlsx возвращает Топ-5 транзакций по сумме платежа"""

    logger.info("Вызвана функция 'get_top_trans'")

    if dframe is None:
        return "Что то не так!"

    list_of_transactions = []

    top5 = dframe.nlargest(5, "Сумма операции с округлением")
    result = top5.sort_values("Дата платежа", ascending=False)

    for index, row in result.iterrows():
        transaction_info = {
            "date": row["Дата платежа"],
            "amount": row["Сумма операции"],
            "category": row["Категория"],
            "description": row["Описание"],
        }

        list_of_transactions.append(transaction_info)

    top_transactions = {"top_transactions": list_of_transactions}

    return json.dumps(top_transactions, ensure_ascii=False)


def get_currency_rates() -> str:
    """Функция возвращает курс валют через API https://app.exchangerate-api.com/"""

    logger.info("Вызвана функция 'get_currency_rates'")

    list_of_currencies = []

    with open(USER_SETTINGS_DIR) as settings:
        data = json.load(settings)

    list_of_cur_acr = data["user_currencies"]

    for currency in list_of_cur_acr:
        response = requests.get(f"https://v6.exchangerate-api.com/v6/{API_KEY_CURRENCY}/latest/{currency}").json()
        list_of_currencies.append({"currency": currency, "rate": round(response["conversion_rates"]["RUB"], 2)})

    currency_rates = {"currency_rates": list_of_currencies}

    return json.dumps(currency_rates, ensure_ascii=False)


def get_stock_price() -> str:
    """Функция возвращает стоимость акций через API https://site.financialmodelingprep.com/"""

    logger.info("Вызвана функция 'get_stock_price'")

    list_of_stock = []

    with open(USER_SETTINGS_DIR) as settings:
        data = json.load(settings)

    list_of_stock_acr = data["user_stocks"]

    for stock in list_of_stock_acr:
        response = requests.get(
            f"https://financialmodelingprep.com/stable/profile?symbol={stock}&apikey={API_KEY_STOCK}"
        ).json()
        list_of_stock.append({"stock": response[0]["symbol"], "price": response[0]["price"]})

    stock_price = {"stock_prices": list_of_stock}

    return json.dumps(stock_price, ensure_ascii=False)
