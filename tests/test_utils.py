from datetime import datetime
from unittest.mock import MagicMock, Mock, patch

import pandas as pd

from src.greet import greeting
from src.utils import currency_rates, get_price_snp500, transaction


@patch("src.greet.datetime")
def test_good_night(mock_datetime: Mock) -> None:
    """Тест для времени ночи."""
    mock_datetime.now.return_value = datetime(2023, 1, 1, 1, 0, 0)  # 1:00
    result = greeting()
    assert result == "Доброй ночи"


@patch("src.greet.datetime")
def test_good_morning(mock_datetime: Mock) -> None:
    """Тест для утра."""
    mock_datetime.now.return_value = datetime(2023, 1, 1, 7, 0, 0)  # 7:00
    result = greeting()
    assert result == "Доброе утро"


@patch("src.greet.datetime")
def test_good_day(mock_datetime: Mock) -> None:
    """Тест для дня."""
    mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0, 0)  # 12:00
    result = greeting()
    assert result == "Добрый день"


@patch("src.greet.datetime")
def test_good_evening(mock_datetime: Mock) -> None:
    """Тест для вечера."""
    mock_datetime.now.return_value = datetime(2023, 1, 1, 19, 0, 0)  # 19:00
    result = greeting()
    assert result == "Добрый вечер"


@patch("pandas.read_excel")
@patch("os.path.exists")
def test_transaction_success(mock_exists: MagicMock, mock_read_excel: MagicMock):
    # Указываем, что файл существует
    mock_exists.return_value = True

    # Создаем тестовый DataFrame
    test_data = {
        "Номер карты": ["1234567890123456", "9876543210987654", "1234567890123456"],
        "Сумма операции": [1000, 2000, 1500],
    }
    test_df = pd.DataFrame(test_data)

    # Настраиваем mock для возврата тестового DataFrame
    mock_read_excel.return_value = test_df

    # Обозначаем путь, который мы будем тестировать
    fake_file_path = "fake_path.xlsx"

    # Вызываем функцию и проверяем результат
    result = transaction(fake_file_path)

    expected_result = [
        {"last_digits": "234567890123456", "total_spent": 2500, "cashback": 25.0},
        {"last_digits": "876543210987654", "total_spent": 2000, "cashback": 20.0},
    ]

    assert result == expected_result


@patch("os.path.exists")
def test_transaction_file_not_found(mock_exists: MagicMock):
    mock_exists.return_value = False
    result = transaction("non_existent_file.xlsx")
    assert result is None


@patch("requests.get")
def test_currency_rates(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"rates": {"EUR": 0.014, "USD": 0.0137}}
    result = currency_rates()
    assert result == [{"currency": "EUR", "rate": 71.43}, {"currency": "USD", "rate": 72.99}]


@patch("requests.get")
def test_get_price_snp500(mock_get):
    # Пример успешных ответов от API для нескольких акций
    responses = [
        {"symbol": "AAPL", "price": 150.12},
        {"symbol": "AMZN", "price": 3173.18},
        {"symbol": "GOOGL", "price": 2742.39},
        {"symbol": "MSFT", "price": 296.71},
        {"symbol": "TSLA", "price": 1007.08},
    ]

    # Настраиваем возврат для каждой акции
    mock_get.side_effect = [
        type("obj", (object,), {"status_code": 200, "json": lambda: responses[0]}),  # AAPL
        type("obj", (object,), {"status_code": 200, "json": lambda: responses[1]}),  # AMZN
        type("obj", (object,), {"status_code": 200, "json": lambda: responses[2]}),  # GOOGL
        type("obj", (object,), {"status_code": 200, "json": lambda: responses[3]}),  # MSFT
        type("obj", (object,), {"status_code": 200, "json": lambda: responses[4]}),  # TSLA
    ]

    # Тестируем полную функцию
    expected = [
        {"stock": "AAPL", "price": 150.12},
        {"stock": "AMZN", "price": 3173.18},
        {"stock": "GOOGL", "price": 2742.39},
        {"stock": "MSFT", "price": 296.71},
        {"stock": "TSLA", "price": 1007.08},
    ]

    result = get_price_snp500()
    assert result == expected, "Ошибка: цены акций не совпадают!"


test_get_price_snp500()
test_transaction_success()
test_transaction_file_not_found()
test_good_night()
test_good_morning()
test_good_day()
test_good_evening()
