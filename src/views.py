import json
import logging
import os

from src.greet import greeting
from src.utils import currency_rates, get_price_snp500, top_transaction, transaction

if not os.path.exists("logs"):
    os.makedirs("logs")

logger = logging.getLogger("views")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(r"logs\\logfile.log")
file_formater = logging.Formatter("%(asctime)s %(filename)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formater)
logger.addHandler(file_handler)

def result_function(date_str: str) -> str:
    result = {
        "greeting": greeting(),
        "cards": transaction(file_path),
        "top_transactions": top_transaction(file_path, date_str),
        "currency_rates": currency_rates(),
        "stock_prices": get_price_snp500(),
    }
    x = json.dumps(result, ensure_ascii=False, indent=3)
    logger.info(f"возврат строки Json: {x}")
    return x


file_path = "C:\\Уроки\\Course\\data\\operations.xlsx"
date_str = "2021-12-30 16:44:00"
print(result_function(date_str))
