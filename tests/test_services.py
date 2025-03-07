from typing import Dict, List

from src.services import filter_description


def test_filter_description(transactions: List[Dict]) -> None:
    # Сначала ищем слово "счет"
    result = filter_description(transactions, "счет")
    assert len(result) == 1, f"Expected 1 transaction, got {len(result)}"
    assert result[0]["description"] == "Перевод со счета на счет", "Не удалось найти правильное описание"
    result_uslugi = filter_description(transactions, "услуг")
    assert len(result_uslugi) == 1, f"Expected 1 transaction for 'услуг', got {len(result_uslugi)}"
    assert result_uslugi[0]["description"] == "Оплата услуг", "Не удалось найти транзакцию с описанием 'Оплата услуг'"
    result_empty = filter_description(transactions, "неизвестное слово")
    assert result_empty == [], "Expected empty result for non-existent word"
