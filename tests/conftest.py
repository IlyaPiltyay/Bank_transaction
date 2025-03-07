from typing import Dict, List

import pytest


@pytest.fixture
def transactions() -> List[Dict]:
    return [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2021-10-01T10:00:00Z",
            "operationAmount": {
                "amount": "1000.00",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Оплата услуг",
            "from": "Счет 123456789",
            "to": "Счет 987654321",
        },
        {
            "id": 2,
            "state": "EXECUTED",
            "date": "2021-10-05T12:30:00Z",
            "operationAmount": {
                "amount": "500.00",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 876543210",
            "to": "Счет 123456789",
        },
        {
            "id": 3,
            "state": "EXECUTED",
            "date": "2021-10-10T14:00:00Z",
            "operationAmount": {
                "amount": "100.00",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Покупка в магазине",
            "from": "Счет 543216789",
            "to": "Счет 987654321",
        },
    ]
