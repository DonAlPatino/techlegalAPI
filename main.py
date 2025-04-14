from pympler import asizeof
import asyncio
from datetime import datetime
import time
import platform

from decouple import config

from credits import saveCredit2db
from db import db_connect
from epexist import saveEpexist2db
from logs import LogRecord
from request import saveRequest2db
from subject import saveSubject2db
from telegram import send_msg
from utils import fetch_all_pages, generate_random_label

tg_token = config('TELEGRAM_BOT_TOKEN')
user_id = int(config('TELEGRAM_CHAT_ID'))
users_ids = [int(id) for id in config('TELEGRAM_CHAT_IDS').split(',')]
token = config('TOKEN')


# Основная функция
def main():
    # Засекаем время начала выполнения программы
    start_time = time.time()
    session = db_connect()
    asyncio.run(send_msg("<pre>Запуск загрузки с техлигал АПИ \n" + f"Хост: {platform.uname()[1]}\n" + f"Дата {datetime.now()}\n" + "</pre>"))
    log_record = LogRecord(slice_tag=generate_random_label(10))
    # Получаем данные из API
    # -------Пример запроса и ответа на получение информации о кредитных договорах и должниках
    # curl -d "token={персональный токен}" https://{фирма}.techlegal.ru/api/getRequest/credit
    base_url = config('BASE_CREDIT_URL')
    results, pages = fetch_all_pages(base_url, token)
    if not results:
        asyncio.run(send_msg(f"<pre>Ошибка получения данных: {base_url} </pre>"))
        print("Не удалось получить данные.")
        return
    log_record.pages = pages
    log_record.records = len(results)
    print(f"CREDIT size: {asizeof.asizeof(results)/(1024 * 1024):.2f} MB")
    saveCredit2db(results, session, log_record)
    # -----Запрос и ответ в формате JSON на получение информации о обращениях в ЕПГУ----
    # curl -d "token={персональный токен}" https://{фирма}.techlegal.ru/api/getRequest/request
    base_url = config('BASE_REQUEST_URL')
    results, pages = fetch_all_pages(base_url, token)
    if not results:
        asyncio.run(send_msg(f"<pre>Ошибка получения данных: {base_url} </pre>"))
        print("Не удалось получить данные.")
        return
    log_record.pages = pages
    log_record.records = len(results)
    print(f"REQUEST size: {asizeof.asizeof(results)/(1024 * 1024):.2f} MB")
    saveRequest2db(results, session, log_record)
    # -----Запрос и ответ в формате JSON на получение информации об имуществе должников----
    # curl -d "token={персональный токен}" https://{фирма}.techlegal.ru/api/getRequest/subject
    base_url = config('BASE_SUBJECT_URL')
    results, pages = fetch_all_pages(base_url, token)
    if not results:
        asyncio.run(send_msg(f"<pre>Ошибка получения данных: {base_url} </pre>"))
        print("Не удалось получить данные.")
        return
    log_record.pages = pages
    log_record.records = len(results)
    print(f"SUBJECT size: {asizeof.asizeof(results)/(1024 * 1024):.2f} MB")
    saveSubject2db(results, session, log_record)

    base_url = config('BASE_EPEXIST_URL')
    inn = config('INN')
    results, pages = fetch_all_pages(base_url, token, inn)
    if not results:
        asyncio.run(send_msg(f"<pre>Ошибка получения данных: {base_url} </pre>"))
        print("Не удалось получить данные.")
        return
    log_record.pages = pages
    log_record.records = len(results)
    print(f"EPEXIST size: {asizeof.asizeof(results)/(1024 * 1024):.2f} MB")
    saveEpexist2db(results, session, log_record)
    # Засекаем время окончания выполнения программы
    end_time = time.time()

    # Вычисляем время выполнения
    execution_time = end_time - start_time
    asyncio.run(send_msg("<pre>Окончание загрузки с техлигал АПИ \n" + f"Хост: {platform.uname()[1]}\n" + f"Дата {datetime.now()}\n" + "</pre>"))
    asyncio.run(send_msg(f"<pre>Время выполнения программы: {execution_time:.2f} секунд</pre>"))


if __name__ == "__main__":
    main()
