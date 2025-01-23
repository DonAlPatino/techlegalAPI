import time

from decouple import config

from credits import saveCredit2db
from db import db_connect
from request import saveRequest2db
from subject import saveSubject2db
from utils import fetch_all_pages

tg_token = config('TELEGRAM_BOT_TOKEN')
user_id = int(config('TELEGRAM_CHAT_ID'))
users_ids = [int(id) for id in config('TELEGRAM_CHAT_IDS').split(',')]
token = config('TOKEN')


# Основная функция
def main():
    # Засекаем время начала выполнения программы
    start_time = time.time()
    session = db_connect()
    # Получаем данные из API
    # -------Пример запроса и ответа на получение информации о кредитных договорах и должниках
    # curl -d "token={персональный токен}" https://{фирма}.techlegal.ru/api/getRequest/credit
    base_url = config('BASE_CREDIT_URL')
    results = fetch_all_pages(base_url, token)
    if not results:
        print("Не удалось получить данные.")
        return
    saveCredit2db(results, session)
    # -----Запрос и ответ в формате JSON на получение информации о обращениях в ЕПГУ----
    # curl -d "token={персональный токен}" https://{фирма}.techlegal.ru/api/getRequest/request
    base_url = config('BASE_REQUEST_URL')
    results = fetch_all_pages(base_url, token)
    if not results:
        print("Не удалось получить данные.")
        return
    saveRequest2db(results, session)
    # -----Запрос и ответ в формате JSON на получение информации об имуществе должников----
    # curl -d "token={персональный токен}" https://{фирма}.techlegal.ru/api/getRequest/subject
    base_url = config('BASE_SUBJECT_URL')
    results = fetch_all_pages(base_url, token)
    if not results:
        print("Не удалось получить данные.")
        return
    saveSubject2db(results, session)

    # Засекаем время окончания выполнения программы
    end_time = time.time()

    # Вычисляем время выполнения
    execution_time = end_time - start_time
    print(f"Время выполнения программы: {execution_time:.2f} секунд")


if __name__ == "__main__":
    main()
