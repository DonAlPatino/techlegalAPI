import asyncio
import time
from typing import Optional
import requests
from decouple import config
from logs import LogRecord
# from telegram import send_msg
# from html import escape
from requests.exceptions import RequestException
from http.client import RemoteDisconnected  # Новый правильный импорт

# Настройка логирования
from log_config import app_logger

# TODO in .env
# Константы
MAX_RETRIES = 3
RETRY_DELAY = 300  # 5 минут
REQUEST_TIMEOUT = 1000


def process_page_data(save_func, session, base_url, log_record: LogRecord, inn=None):
    total_pages = 0
    total_records = 0

    # check for first_page_url, get number of pages

    # Формируем URL для первой страницы
    first_page_url = build_page_url(base_url, 1, inn)

    # Запрашиваем первую страницу
    total_records, total_pages, size = process_page_with_retry(save_func, session, log_record, first_page_url, 0, total_pages,
                                                         total_records)
    # Проверяем количество страниц
    # total_pages = first_page_data.get("pages", 1)
    app_logger.info(f"Кол-во страниц для запроса {base_url}: составляет {total_pages}")
    print(f"{first_page_url} object size: {size / (1024 * 1024):.2f} MB")

    # Если страниц больше одной, запрашиваем остальные
    if total_pages > 1:
        page = 2
        while page <= total_pages:
            page_url = build_page_url(base_url, page, inn)

            total_records, total_pages, size = process_page_with_retry(save_func, session, log_record, page_url, page,
                                                                       total_pages, total_records)
            print(f"{page_url} object size: {size / (1024 * 1024):.2f} MB")
            # Переход к следующей странице в любом случае
            page += 1
    return total_records, total_pages


def process_page_with_retry(save_func, session, log_record: LogRecord, page_url, page, total_pages, total_records):
    token = config('TOKEN')
    data = {
        "token": token
    }
    results = []
    retries = 0
    max_retries = MAX_RETRIES
    req_total_pages = 0
    size = 0
    while retries < max_retries:
        try:
            response = requests.post(page_url, data=data, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()  # Проверяем HTTP-ошибки
        except RemoteDisconnected as e:
            app_logger.error(
                f"Attempt {retries}/{max_retries} failed: Connection closed by server. Retrying...")
            retries += 1
            time.sleep(RETRY_DELAY)  # Увеличиваем задержку с каждой попыткой

        except RequestException as e:
            app_logger.error(f"Attempt {retries}/{max_retries} failed: {str(e)}")
            retries += 1
            time.sleep(RETRY_DELAY)

        if response.status_code != 200:
            app_logger.error(f"Attempt {retries}/{max_retries} failed for {page}: {response.status_code}")
            retries += 1
            time.sleep(RETRY_DELAY)  # Ждём перед повторной попыткой

        try:
            page_data = response.json()
            results = page_data.get("result", [])
            total_records = total_records + len(results)
            req_total_pages = page_data.get("pages", 1)
            # all_results.extend(page_data.get("result", []))
        except ValueError as e:  # Ловим как ValueError (для requests<2.27) или RequestsJSONDecodeError
            handle_json_decode_error(response, e, retries + 1)
            retries += 1
            app_logger.error(f"Attempt {retries}/{max_retries} failed for {page}: {str(e)}")
            time.sleep(RETRY_DELAY)  # Ждём перед повторной попыткой

        # check for 0 records in answer.

        if len(results) != 0 and req_total_pages:
            size = save_func(results, session, log_record)
            session.flush()
            if req_total_pages > total_pages:
                if total_pages == 0:
                    total_pages = req_total_pages
                    app_logger.info(
                        f"Установлено кол-во страниц в ответе на странице {page} -  {req_total_pages} страниц")
                else:
                    total_pages = req_total_pages
                    app_logger.warning(
                        f"Изменилось кол-во страниц в ответе на странице {page} - стало {req_total_pages}/{total_pages} страниц")
            break
        else:
            retries += 1
            app_logger.error(f"Attempt {retries}/{max_retries} failed for {page}: 0 records in answer detect")
            time.sleep(RETRY_DELAY)  # Ждём перед повторной попыткой

    # Исчерпали ретраи - выходим из забора endpoint без сохранения
    if retries >= max_retries:
        app_logger.error(f"Исчерпано кол-во попыток (попытка {retries}) для {page}")
        return 0, 0, 0
    return total_records, total_pages, size


def handle_json_decode_error(response, error, retry_count: int) -> None:
    """Обрабатывает ошибку декодирования JSON и логирует её."""
    error_msg = (
        f"Ошибка декодирования JSON (попытка {retry_count}).\n"
        f"{error}.\n"
        f"Начало ответа: {response.text[:200]}\n"
        f"Конец ответа: {response.text[-100:]}"
    )
    app_logger.error(error_msg)
    # TODO
    # safe_text = escape(error_msg)
    # asyncio.run(send_msg(f"{safe_text}", parse_mode='Markdown'))
    # Сохраняем сырой ответ
    with open("response_raw.txt", "w", encoding="utf-8") as file:
        file.write(response.text)


def build_page_url(base_url: str, page: int, inn: Optional[str] = None) -> str:
    """Строит URL для запроса с учётом номера страницы и INN."""
    if inn:
        return f"{base_url}/{page}?inn={inn}"
    return f"{base_url}/{page}"
