import json
import logging
import os
from datetime import datetime, timedelta
from typing import Any, Callable, Hashable

import pandas as pd

if not os.path.exists("logs"):
    os.makedirs("logs")

logger = logging.getLogger("views")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(r"logs\\logfile_reports.log")
file_formater = logging.Formatter("%(asctime)s %(filename)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formater)
logger.addHandler(file_handler)


def report_to_file(filename: str) -> Callable:
    """Декоратор для записи результата функции в файл с заданным именем."""

    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)

            # Проверяем, существует ли файл
            file_exists = os.path.exists(filename)
            with open(filename, "a", encoding="utf-8") as f:
                logger.info(f"Запись результата в файл: {filename}")
                if file_exists:
                    f.write(",\n")  # Добавляем запятую для корректного формата JSON
                json.dump(result, f, ensure_ascii=False, indent=4)

            return result

        return wrapper

    return decorator


@report_to_file("report.json")
def spending_by_category(transactions: pd.DataFrame, category: str, date: datetime) -> list[dict[Hashable, Any]]:
    if date is None:
        date = datetime.now().date()
    try:
        date = pd.to_datetime(date, dayfirst=True)
    except ValueError:
        logger.error(f"Неверный формат даты:  {date}")
        raise ValueError("Invalid date format. Please use 'DD.MM.YYYY'.")

    print(f"Для фильтрации параметров: Категория: {category}, Дата: {date}")  # Для отладки

    # Преобразование даты
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], dayfirst=True)

    filtered_transactions = transactions[transactions["Категория"] == category]

    # Выводим для отладки, сколько записей отфильтровано по категории
    print(f"Записи по категории '{category}':")
    print(filtered_transactions)

    start_date = date - timedelta(days=90)
    end_date = date

    print(f"Start Date: {start_date}, End Date: {end_date}")  # Отладочный вывод

    recent_transactions = filtered_transactions[
        (filtered_transactions["Дата операции"] >= start_date) & (filtered_transactions["Дата операции"] <= end_date)
    ]

    # Преобразуем даты в строки для сериализации
    result = recent_transactions.to_dict("records")

    for item in result:
        if isinstance(item["Дата операции"], pd.Timestamp):
            item["Дата операции"] = item["Дата операции"].strftime("%d.%m.%Y")

    print(f"Filtered Transactions: {result}")  # Отладочный вывод

    return result


file_path = "C:\\Уроки\\Course\\data\\operations.xlsx"

# print(spending_by_category(pd.read_excel(file_path), "Фастфуд", "11.11.2019"))
