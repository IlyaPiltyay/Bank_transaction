import pandas as pd

from src.greet import greeting
from src.reports import spending_by_category
from src.utils import currency_rates, file_path, get_price_snp500, top_transaction, transaction
from src.views import date_str


def main_function() -> None:
    """Функция объеденят все модули"""
    print(f"Приветствие {greeting()} ")
    print(f"Карты,Кэшбэк {transaction(file_path)}")
    print(f"Топ Транзакций {top_transaction(file_path, date_str)}")
    print(f"Курсы вадют {currency_rates()}")
    print(f"Курсы акций {get_price_snp500()}")
    print(f"Отчеты {spending_by_category(pd.read_excel(file_path), "Фастфуд", "11.11.2019")}")


if __name__ == "__main__":
    main_function()
