import json
from unittest.mock import patch

from src.views import get_main_json_answer


@patch("requests.get")
def test_get_main_json_answer(mock_requests):
    mock_requests.return_value.json.return_value = [{"symbol": "AAL", "price": 221},
                                                    {"conversion_rates": {"USD": 13.444, "RUB": 111.3222}}]

    assert get_main_json_answer("2021-12-30 01:00:00") == json.dumps({
        "greeting": "Доброй ночи",
        "cards": [{"last_digits": "7197", "total_spent": -23538.8, "cashback": -235.39},
                  {
                      "last_digits": "5091",
                      "total_spent": -12179.99,
                      "cashback": -121.8
                  },
                  {
                      "last_digits": "4556",
                      "total_spent": 198770.3,
                      "cashback": 1987.7
                  }
                  ],
        "top_transactions": [
            {
                "date": "30.12.2021",
                "amount": 174000.0,
                "category": "Пополнения",
                "description": "Пополнение через Газпромбанк"
            },
            {
                "date": "23.12.2021",
                "amount": 28001.94,
                "category": "Переводы",
                "description": "Перевод Кредитная карта. ТП 10.2 RUR"
            },
            {
                "date": "23.12.2021",
                "amount": 20000.0,
                "category": "Другое",
                "description": "Иван С."
            },
            {
                "date": "31.12.2021",
                "amount": -20000.0,
                "category": "Переводы",
                "description": "Константин Л."
            },
            {
                "date": "23.12.2021",
                "amount": -28001.94,
                "category": "Переводы",
                "description": "Перевод Кредитная карта. ТП 10.2 RUR"
            }
        ],
        "currency_rates": [
            {}
        ],
        "stock_prices": [
            {
                "stock": "AAL",
                "price": 221
            }
        ]
    }, ensure_ascii=False, indent=4)
