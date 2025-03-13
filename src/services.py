import re
from typing import Dict, List

transactions = [
    {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {
            "amount": "9824.07",
            "currency": {"name": "USD", "code": "USD"},
        },
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702",
    },
    {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {
            "amount": "79114.93",
            "currency": {"name": "USD", "code": "USD"},
        },
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "to": "Счет 75651667383060284188",
    },
]


def filter_description(banking_description: List[Dict], word: str) -> List[Dict]:
    """Функция принимает список словарей с данными о банковских операциях и строку поиска,
    а возвращает список словарей, у которых в описании есть данная строка."""
    if not word:  # Если слово пустое, сразу возвращаем пустой список
        return []

    filtered_list = []
    pattern = re.compile(rf"\b{word}\b", re.IGNORECASE)

    for transaction in banking_description:
        if "description" in transaction and isinstance(transaction["description"], str):
            # Поиск заданного слова в описании
            if pattern.search(transaction["description"]):
                filtered_list.append(transaction)
    return filtered_list


print(filter_description(transactions, word="Перевод"))
