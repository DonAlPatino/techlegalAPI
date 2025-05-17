import time
from typing import Optional
import requests
from decouple import config
from logs import LogRecord
# from html import escape
from requests.exceptions import RequestException, Timeout
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
    has_error = False

    # check for first_page_url, get number of pages

    # Формируем URL для первой страницы
    first_page_url = build_page_url(base_url, 1, inn)

    # Запрашиваем первую страницу
    total_records, total_pages, size = process_page_with_retry(save_func, session, log_record, first_page_url, 0,
                                                               total_pages, total_records)
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
            if size == 0:
                has_error = True
    return total_records, total_pages, has_error


def process_page_with_retry(save_func, session, log_record: LogRecord, page_url, page, total_pages, total_records):
    token = config('TOKEN')
    data = {
        "token": token
    }
    retries = 0
    max_retries = MAX_RETRIES
    size = 0
    while retries < max_retries:
        try:
            response = requests.post(page_url, data=data, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()  # Проверяем HTTP-ошибки

            # Проверяем, что ответ не пустой (например, нет тела ответа или оно состоит только из пробелов)
            if not response.text.strip():
                raise ValueError("Empty response content")

        # except (Timeout, ConnectionError, RemoteDisconnected, RequestException) as e:
        #     retries += 1
        #     error_type = "timeout" if isinstance(e, Timeout) else \
        #         "connection error" if isinstance(e, ConnectionError) else \
        #             "server disconnect" if isinstance(e, RemoteDisconnected) else \
        #                 "empty response" if isinstance(e, ValueError) else "request failed"
        except Exception as e:  # Ловим ВСЕ исключения
            retries += 1

            # Определяем тип ошибки
            error_type = (
                "timeout" if isinstance(e, Timeout) else
                "connection error" if isinstance(e, ConnectionError) else
                "server disconnect" if isinstance(e, RemoteDisconnected) else
                "Request Exception" if isinstance(e, RequestException) else
                "empty response" if isinstance(e, ValueError) else
                f"unexpected error ({type(e).__name__})"  # Добавляем имя класса для неизвестных ошибок
            )

            app_logger.error(f"Attempt {retries}/{max_retries} {error_type}: {str(e)}")
            time.sleep(RETRY_DELAY)  # Увеличиваем задержку с каждой попыткой
            continue

        if response.status_code != 200:
            app_logger.error(f"Attempt {retries}/{max_retries} failed for {page}: {response.status_code}")
            retries += 1
            time.sleep(RETRY_DELAY)  # Ждём перед повторной попыткой
            continue

        try:
            page_data = response.json()
            if not isinstance(page_data, dict):
                raise ValueError("Page_data in response is not a valid JSON object")
            results = page_data.get("result", [])
            # if not isinstance(results, dict):
            #     raise ValueError("results in response is not a valid JSON object")
            total_records = total_records + len(results)
            req_total_pages = page_data.get("pages", 1)

        except ValueError as e:  # Ловим как ValueError (для requests<2.27) или RequestsJSONDecodeError
            # Сохраняем сырой ответ
            with open("response_raw.txt", "w", encoding="utf-8") as file:
                file.write(response.text)
            handle_json_decode_error(response, e, retries + 1)
            retries += 1
            app_logger.error(f"Attempt {retries}/{max_retries} failed for {page}: {str(e)}")
            time.sleep(RETRY_DELAY)  # Ждём перед повторной попыткой
            continue

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
                        f"Изменилось кол-во страниц в ответе на странице {page} - "
                        f"стало {req_total_pages}/{total_pages} страниц")
            break
        else:
            retries += 1
            app_logger.error(f"Attempt {retries}/{max_retries} failed for {page}: 0 records in answer detect. "
                             f"Response code:{response.status_code}")
            # Сохраняем сырой ответ
            with open("response_raw.txt", "w", encoding="utf-8") as file:
                file.write(response.text)
            time.sleep(RETRY_DELAY)  # Ждём перед повторной попыткой
            continue

    # Исчерпали ретраи - выходим из забора endpoint без сохранения
    if retries >= max_retries:
        app_logger.error(f"Исчерпано кол-во попыток (попытка {retries}) для {page}")

        return total_records, total_pages, 0
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


def build_page_url(base_url: str, page: int, inn: Optional[str] = None) -> str:
    """Строит URL для запроса с учётом номера страницы и INN."""
    if inn:
        return f"{base_url}/{page}?inn={inn}"
    return f"{base_url}/{page}"
