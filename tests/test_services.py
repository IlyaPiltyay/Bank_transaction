from typing import Dict, List

import pytest

from src.services import filter_description


@pytest.mark.parametrize(
    "banking_description, word, expected",
    [
        (
            [
                {"id": 1, "description": "Перевод организации"},
                {"id": 2, "description": "Зарплата за июль"},
                {"id": 3, "description": "Перевод со счета"},
            ],
            "Перевод",
            [{"id": 1, "description": "Перевод организации"}, {"id": 3, "description": "Перевод со счета"}],
        ),
        (
            [
                {"id": 1, "description": "Перевод организации"},
                {"id": 2, "description": "Зарплата за июль"},
            ],
            "Деньги",
            [],
        ),
        ([], "Перевод", []),
        (
            [
                {"id": 1, "description": "Перевод организации"},
                {"id": 2, "description": "Зарплата за июль"},
            ],
            "",
            [],
        ),
    ],
)
def test_filter_description(banking_description: List[Dict], word: str, expected: List[Dict]) -> None:

    assert filter_description(banking_description, word) == expected
