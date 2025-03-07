import logging
import os
from datetime import datetime


if not os.path.exists("logs"):
    os.makedirs("logs")

logger = logging.getLogger("views")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(r"logs\\logfile.log")
file_formater = logging.Formatter("%(asctime)s %(filename)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formater)
logger.addHandler(file_handler)

def greeting() -> str:
    """Возвращает приветствие в зависимости от времени суток."""
    current_hour = datetime.now().hour  # Получаем текущий час
    logger.info(f"Приветстиве от текущего времени: {current_hour}")
    if 0 <= current_hour <= 3:
        return "Доброй ночи"
    elif 4 <= current_hour <= 10:
        return "Доброе утро"
    elif 11 <= current_hour <= 16:
        return "Добрый день"
    else:
        return "Добрый вечер"
