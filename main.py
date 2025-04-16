import asyncio
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
from telegram import send_msg
from utils import generate_random_label
from process_page_data import process_page_data


# Основная функция
def main():
    # Засекаем время начала выполнения программы
    start_time = time.time()
    session = db_connect()
    asyncio.run(send_msg(
        "<pre>Запуск загрузки с техлигал АПИ \n" + f"Хост: {platform.uname()[1]}\n" + f"Дата {datetime.now()}\n" + "</pre>"))
    log_record = LogRecord(slice_tag=generate_random_label(10))
    # Получаем данные из API
    # -------Пример запроса и ответа на получение информации о кредитных договорах и должниках
    # curl -d "token={персональный токен}" https://{фирма}.techlegal.ru/api/getRequest/credit
    base_url = config('BASE_CREDIT_URL')
    total_records, total_pages = process_page_data(saveCredit2db, session, base_url, log_record)
    if not total_records:
        asyncio.run(send_msg(f"<pre>Ошибка получения данных: {base_url} </pre>"))
        print("Не удалось получить данные.")
        return
    log_record.pages = total_pages
    log_record.records = total_records
    # saveCredit2db(results, session, log_record)
    log_record.tablename = "techlegal_credits"
    save_to_database(session, log_record)
    # # -----Запрос и ответ в формате JSON на получение информации о обращениях в ЕПГУ----
    # # curl -d "token={персональный токен}" https://{фирма}.techlegal.ru/api/getRequest/request
    base_url = config('BASE_REQUEST_URL')
    total_records, total_pages = process_page_data(saveRequest2db, session, base_url, log_record)
    if not total_records:
        asyncio.run(send_msg(f"<pre>Ошибка получения данных: {base_url} </pre>"))
        print("Не удалось получить данные.")
        return
    log_record.pages = total_pages
    log_record.records = total_records

    # saveRequest2db(results, session, log_record)
    # Сохраняем изменения в БД
    log_record.tablename = "techlegal_requests"
    save_to_database(session, log_record)
    # # -----Запрос и ответ в формате JSON на получение информации об имуществе должников----
    # # curl -d "token={персональный токен}" https://{фирма}.techlegal.ru/api/getRequest/subject
    base_url = config('BASE_SUBJECT_URL')
    total_records, total_pages = process_page_data(saveSubject2db, session, base_url, log_record)
    if not total_records:
        asyncio.run(send_msg(f"<pre>Ошибка получения данных: {base_url} </pre>"))
        print("Не удалось получить данные.")
        return
    log_record.pages = total_pages
    log_record.records = total_records

    # saveSubject2db(results, session, log_record)
    # Сохраняем изменения в БД
    log_record.tablename = "techlegal_subjects"
    save_to_database(session, log_record)
    # ================================
    base_url = config('BASE_EPEXIST_URL')
    inn = config('INN')
    total_records, total_pages = process_page_data(saveEpexist2db, session, base_url, log_record, inn)
    if not total_records:
        asyncio.run(send_msg(f"<pre>Ошибка получения данных: {base_url} </pre>"))
        print("Не удалось получить данные.")
        return
    log_record.pages = total_pages
    log_record.records = total_records

    # saveEpexist2db(results, session, log_record)
    # Сохраняем изменения в БД
    log_record.tablename = "techlegal_epexist"
    save_to_database(session, log_record)
    # Засекаем время окончания выполнения программы
    end_time = time.time()

    # Вычисляем время выполнения
    execution_time = end_time - start_time
    asyncio.run(send_msg(
        "<pre>Окончание загрузки с техлигал АПИ \n" + f"Хост: {platform.uname()[1]}\n" + f"Дата {datetime.now()}\n" + "</pre>"))
    asyncio.run(send_msg(f"<pre>Время выполнения программы: {execution_time:.2f} секунд</pre>"))


if __name__ == "__main__":
    main()
