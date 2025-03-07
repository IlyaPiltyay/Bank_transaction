import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

import pandas as pd
import requests
from dotenv import load_dotenv


def transaction(file_path: str) -> Optional[List[Dict[str, float]]]:
    if not os.path.exists(file_path):
        print("файл не найден.")
        return None

    df = pd.read_excel(file_path)
    df["Номер карты"] = df["Номер карты"].str[1:]
    # Группировка по номеру карты и суммирование операций
    summary = df.groupby("Номер карты")["Сумма операции"].sum().reset_index()
    # Рассчитываем кэшбэк
    summary["cashback"] = (summary["Сумма операции"] // 100).astype(float)
    summary["cashback"] = summary["cashback"].round(2)
    result = []
    for index, row in summary.iterrows():
        last_digits = row.get("Номер карты", " ")
        total_spent = row.get("Сумма операции", " ")
        cashback = row.get("cashback", " ")
        result.append({"last_digits": last_digits, "total_spent": total_spent, "cashback": cashback})

    return result
#print(transaction(file_path = "C:\\Уроки\\Course\\data\\operations.xlsx"))

def top_transaction(file_path: str, date_str: str) -> Optional[List[Dict[str, float]]]:
    df = pd.read_excel(file_path)
    # Преобразование столбца "Дата платежа" в тип datetime
    df["Дата платежа"] = pd.to_datetime(df["Дата платежа"], dayfirst=True, errors="coerce")
    top_transaction_df = df.sort_values(by="Сумма операции", ascending=False)

    # Преобразование строки даты в объект datetime
    input_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")  # Ожидаем нужный формат
    start_date = input_date.replace(day=1)
    result_date = top_transaction_df[
        (top_transaction_df["Дата платежа"] >= start_date) & (top_transaction_df["Дата платежа"] <= input_date)
    ]
    top_transaction_five = result_date.head(5)

    total_five = []
    for index, row in top_transaction_five.iterrows():
        payment_date = row["Дата платежа"].strftime("%d.%m.%Y")
        amount = row.get("Сумма операции", " ")
        category = row.get("Категория", " ")
        description = row.get("Описание", " ")
        total_five.append({"date": payment_date, "amount": amount, "category": category, "description": description})

    return total_five


file_path = "C:\\Уроки\\Course\\data\\operations.xlsx"

load_dotenv("C:\\Уроки\\Course\\.env")
API_KEY = os.getenv("API_KEY")


def currency_rates() -> Optional[List[Dict[Any, Any]]]:

    url = "https://api.apilayer.com/exchangerates_data/latest?base=RUB&symbols=EUR,USD"
    headers = {"apikey": API_KEY}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            rates = []
            if "EUR" in data["rates"]:
                eur_to_rub = round(1 / data["rates"]["EUR"], 2)
                rates.append({"currency": "EUR", "rate": eur_to_rub})

            if "USD" in data["rates"]:
                usd_to_rub = round(1 / data["rates"]["USD"], 2)
                rates.append({"currency": "USD", "rate": usd_to_rub})
                user_settings = {
                    "user_currencies": ["USD", "EUR"],
                    "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"],
                }
                with open("C:\\Уроки\\Course\\user_settings.json", "w", encoding="utf8") as file:
                    json.dump(user_settings, file)
            return rates
        else:
            print(f"Ошибка: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        print(f"Возникла ошибка: {e}")
        return None


# Выводим результаты
#print(currency_rates())

API_KEY_stocks = "6325934a56084b0e8c2979172ecf89c1"
load_dotenv("C:\\Уроки\\Course\\.env")
API_KEY_stocks = os.getenv("API_KEY_stocks")


def get_price_snp500() -> dict:
    """
    Функция, которая извлекает цены акций из списка S&P 500
    путем вызова внешнего API.
    """
    stocks_list = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    price_stocks = []

    for stock in stocks_list:
        # Получаем данные по текущей цене акций
        response = requests.get(f"https://api.twelvedata.com/price?symbol={stock}&apikey={API_KEY_stocks}")

        # Проверяем, успешен ли запрос
        if response.status_code == 200:
            dict_result = response.json()
            # Извлекаем цену
            price_element = dict_result.get("price")
            if price_element is not None:
                # Добавляем словарь с информацией о акции в список
                price_stocks.append({"stock": stock, "price": price_element})

            else:
                print(f"Не удалось получить цену для {stock}.")  # Уведомление об ошибке
        else:
            print(f"Ошибка при получении данных для {stock}: {response.status_code}")

    return price_stocks



# Вызов функции и вывод результата
# print(get_price_snp500())
