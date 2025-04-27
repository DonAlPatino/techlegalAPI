from datetime import datetime
import time
import platform
from decouple import config
from credits import saveCredit2db
from db import db_connect, save_to_database
from epexist import saveEpexist2db
from logs import LogRecord
from request import saveRequest2db
from subject import saveSubject2db
from utils import generate_random_label
from process_page_data import process_page_data
from log_config import setup_logging
from easy_async_tg_notify import Notifier

env = config('ENV')
token = config('TELEGRAM_BOT_TOKEN')
user_id = int(config('TELEGRAM_CHAT_ID'))
users_ids = [int(id) for id in config('TELEGRAM_CHAT_IDS').split(',')]
recipient = users_ids[0] if env == "dev" else users_ids[1]

# Создаем Notifier один раз
tg_notifier = Notifier(token)
chat_id = recipient

# Инициализируем логгер с Telegram
app_logger = setup_logging(telegram_notifier=tg_notifier, telegram_chat_id=chat_id)


# Основная функция
def main():
    # Засекаем время начала выполнения программы
    start_time = time.time()
    session = db_connect()
    app_logger.info(
        f"Запуск загрузки с техлигал АПИ \n" + f"Хост: {platform.uname()[1]}\n" + f"Дата {datetime.now()}\n")
    log_record = LogRecord(slice_tag=generate_random_label(10))

    # Определяем коллекцию endpoints с параметрами
    endpoints = [
        # curl -d "token={персональный токен}" https://{фирма}.techlegal.ru/api/getRequest/credit
        {
            'url': 'BASE_CREDIT_URL',
            'save_func': saveCredit2db,
            'tablename': 'techlegal_credits',
            'extra_args': None
        },
        # curl -d "token={персональный токен}" https://{фирма}.techlegal.ru/api/getRequest/request
        {
            'url': 'BASE_REQUEST_URL',
            'save_func': saveRequest2db,
            'tablename': 'techlegal_requests',
            'extra_args': None
        },
        # curl -d "token={персональный токен}" https://{фирма}.techlegal.ru/api/getRequest/subject
        {
            'url': 'BASE_SUBJECT_URL',
            'save_func': saveSubject2db,
            'tablename': 'techlegal_subjects',
            'extra_args': None
        },
        {
            'url': 'BASE_EPEXIST_URL',
            'save_func': saveEpexist2db,
            'tablename': 'techlegal_epexist',
            'extra_args': config('INN')
        }
    ]

    # Обрабатываем каждый endpoint в цикле
    for endpoint in endpoints:
        base_url = config(endpoint['url'])
        total_records, total_pages, has_error = process_page_data(
            endpoint['save_func'],
            session,
            base_url,
            log_record,
            endpoint['extra_args']
        )

        # Обновляем и сохраняем log_record
        log_record.pages = total_pages
        log_record.records = total_records
        log_record.tablename = endpoint['tablename']
        log_record.has_error = has_error
        save_to_database(session, log_record)

    # Засекаем время окончания выполнения программы
    end_time = time.time()

    # Вычисляем время выполнения
    execution_time = end_time - start_time
    app_logger.info(
        f"Окончание загрузки с техлигал АПИ \n" + f"Хост: {platform.uname()[1]}\n" + f"Дата {datetime.now()}\n")
    app_logger.info(f"Время выполнения программы: {execution_time:.2f} секунд")


if __name__ == "__main__":
    main()
