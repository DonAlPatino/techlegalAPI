import asyncio
import time
from typing import Optional
import logging
import requests
from decouple import config
from logs import LogRecord
from telegram import send_msg
from html import escape

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Константы
MAX_RETRIES = 3
RETRY_DELAY = 300  # 5 минут
REQUEST_TIMEOUT = 1000


def process_page_data(save_func, session, base_url, log_record: LogRecord, inn=None):
    token = config('TOKEN')
    data = {
        "token": token
    }
    results = []

    # Формируем URL для первой страницы
    first_page_url = build_page_url(base_url, 1, inn)

    # Запрашиваем первую страницу
    response = requests.post(first_page_url, data=data)
    if response.status_code != 200:
        error_msg = (
            f"Ошибка при выполнении запроса {first_page_url}: {response.status_code}."
        )
        asyncio.run(send_msg(f"<pre>{error_msg}</pre>"))
        logger.error(error_msg)
        return None
    try:
        first_page_data = response.json()
        results.extend(first_page_data.get("result", []))
        save_func(results, session, log_record)
        total_records = len(results)
    except ValueError as e:  # Ловим как ValueError (для requests<2.27) или RequestsJSONDecodeError
        handle_json_decode_error(response, e, 1)
        return 0, 0

    # Проверяем количество страниц
    total_pages = first_page_data.get("pages", 1)
    error_msg = (
        f"Кол-во страниц для запроса {base_url}: составляет {total_pages}"
    )
    asyncio.run(send_msg(f"<pre>{error_msg}</pre>"))
    logger.error(error_msg)

    # Если страниц больше одной, запрашиваем остальные
    if total_pages > 1:
        for page in range(2, total_pages + 1):
            page_url = build_page_url(base_url, page, inn)

            retries = 0
            max_retries = MAX_RETRIES

            while retries < max_retries:
                response = requests.post(page_url, data=data, timeout=REQUEST_TIMEOUT)

                if response.status_code != 200:
                    error_msg = (
                        f"Ошибка при выполнении запроса для страницы {page}: {response.status_code}"
                    )
                    asyncio.run(send_msg(
                        f"<pre> {error_msg} </pre>"))
                    logger.error(error_msg)
                    retries += 1
                    time.sleep(RETRY_DELAY)  # Ждём перед повторной попыткой

                try:
                    page_data = response.json()
                    # all_results.extend(page_data.get("result", []))
                    results = page_data.get("result", [])
                    save_func(results, session, log_record)
                    total_records = total_records + len(results)
                    session.flush()
                    req_total_pages = page_data.get("pages", 1)
                    if req_total_pages > total_pages:
                        total_pages = req_total_pages
                        error_msg = (
                            f"Изменилось кол-во страниц в ответе на странице {page} - стало {req_total_pages} страниц"
                        )
                        asyncio.run(send_msg(f"<pre>{error_msg}</pre>"))
                        logger.error(error_msg)
                    break
                except ValueError as e:  # Ловим как ValueError (для requests<2.27) или RequestsJSONDecodeError
                    handle_json_decode_error(response, e, retries + 1)
                    retries += 1
                    error_msg = (
                        f"Ошибка при выполнении запроса для страницы {page}: {response.status_code}.(попытка {retries + 1})"
                    )
                    asyncio.run(send_msg(f"<pre>{error_msg}</pre>"))
                    logger.error(error_msg)
                    time.sleep(RETRY_DELAY)  # Ждём перед повторной попыткой
            if retries >= max_retries:
                error_msg = (
                    f"Исчерпано кол-во попыток (попытка {retries})"
                )
                asyncio.run(send_msg(f"<pre>{error_msg}</pre>"))
                logger.error(error_msg)
                return 0, 0

    return total_records, total_pages


def handle_json_decode_error(response, error, retry_count: int) -> None:
    """Обрабатывает ошибку декодирования JSON и логирует её."""
    error_msg = (
        f"Ошибка декодирования JSON (попытка {retry_count}).\n"
        f"{error}.\n"
        f"Начало ответа: {response.text[:200]}\n"
        f"Конец ответа: {response.text[-100:]}"
    )
    logger.error(error_msg)
    # TODO
    # asyncio.run(send_msg(f"<pre>{error_msg}</pre>"))
    safe_text = escape(error_msg)
    asyncio.run(send_msg(f"{safe_text}<"))
    # Сохраняем сырой ответ
    with open("response_raw.txt", "w", encoding="utf-8") as file:
        file.write(response.text)


def build_page_url(base_url: str, page: int, inn: Optional[str] = None) -> str:
    """Строит URL для запроса с учётом номера страницы и INN."""
    if inn:
        return f"{base_url}/{page}?inn={inn}"
    return f"{base_url}/{page}"
