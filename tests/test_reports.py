import os

import pandas as pd

from src.reports import spending_by_category


def test_spending_by_category():
    # Создаем тестовый DataFrame
    test_data = {
        'Дата операции': ['01.01.2023', '15.01.2023', '20.12.2022', '01.03.2023'],
        'Категория': ['Фастфуд', 'Фастфуд', 'Развлечение', 'Фастфуд'],
        'Сумма': [100, 200, 150, 300],
    }
    transactions_df = pd.DataFrame(test_data)
    # Преобразование колонки с датами в правильный формат
    transactions_df['Дата операции'] = pd.to_datetime(transactions_df['Дата операции'], dayfirst=True)


    results = spending_by_category(transactions_df, 'Фастфуд', '01.04.2023')
    assert len(results) > 0, "Ошибка: не получены транзакции для категории 'Фастфуд'"

    results = spending_by_category(transactions_df, 'Развлечение', '01.04.2023')
    assert len(results) == 0, "Ошибка: не получены транзакции для категории 'Развлечение'"



test_spending_by_category()


