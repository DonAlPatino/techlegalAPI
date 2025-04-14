from datetime import datetime
import requests
import asyncio

from telegram import send_msg
import random
import string


def check_answer(records: int, pages: int, records_per_page: int):
    """
    Функция для проверки полученных от API данных.

    :param records: Кол-во возвращенных записей
    :param pages: Кол-во возвращенных страниц
    :param records_per_page: Кол-во записей на странице
    :return: True, если records находится между (pages - 1) * records_per_page и pages * records_per_page, иначе False
    """
    lower_bound = (pages - 1) * records_per_page
    upper_bound = pages * records_per_page

    return lower_bound <= records <= upper_bound


def generate_random_label(length=8):
    characters = string.ascii_letters + string.digits  # Используем буквы и цифры
    random_label = ''.join(random.choice(characters) for _ in range(length))
    return random_label


# Функция для выполнения запроса к API
def fetch_all_pages(base_url, token, inn=None):
    data = {
        "token": token
    }
    all_results = []

    # Формируем URL для первой страницы
    if inn:
        first_page_url = f"{base_url}/1?inn={inn}"  # Добавляем INN как параметр
    else:
        first_page_url = base_url  # Обычный URL без параметров

    # Запрашиваем первую страницу
    response = requests.post(first_page_url, data=data)
    if response.status_code != 200:
        asyncio.run(send_msg(f"<pre>Ошибка при выполнении запроса {first_page_url}: {response.status_code} </pre>"))
        print(f"Ошибка при выполнении запроса: {response.status_code}")
        return None

    first_page_data = response.json()
    all_results.extend(first_page_data.get("result", []))

    # Проверяем количество страниц
    total_pages = first_page_data.get("pages", 1)
    asyncio.run(send_msg(f"<pre>Кол-во страниц для запроса {base_url}: составляет {total_pages} </pre>"))
    print(f"Кол-во страниц для запроса {base_url} составляет {total_pages}")

    # Если страниц больше одной, запрашиваем остальные
    if total_pages > 1:
        for page in range(2, total_pages + 1):
            # print(f"Обрабатываю страницу {page} из {total_pages}")
            if inn:
                # Номер страницы в пути, INN в параметрах
                page_url = f"{base_url}/{page}?inn={inn}"
            else:
                # Обычный URL с номером страницы в пути
                page_url = f"{base_url}/{page}"
            response = requests.post(page_url, data=data)
            if response.status_code == 200:
                page_data = response.json()
                all_results.extend(page_data.get("result", []))
                req_total_pages = page_data.get("pages", 1)
                if req_total_pages > total_pages:
                    total_pages = req_total_pages
                    asyncio.run(send_msg(
                        f"<pre>Изменилось кол-во страниц в ответе на странице {page} - стало {req_total_pages} страниц</pre>"))
                    print(f"Изменилось кол-во страниц в ответе на странице {page} - стало {req_total_pages} страниц")
            else:
                asyncio.run(
                    send_msg(f"<pre>Ошибка при выполнении запроса для страницы {page}: {response.status_code} </pre>"))
                print(f"Ошибка при выполнении запроса для страницы {page}: {response.status_code}")

    return all_results, total_pages


def convert_date(date_str):
    """
    Конвертирует дату из формата DD.MM.YYYY в YYYY-MM-DD.
    Если дата уже в формате YYYY-MM-DD, возвращает её без изменений.
    Если дата некорректна или пуста, возвращает None.
    """
    if not date_str or date_str == "00.00.0000":
        return None

    # Проверяем, соответствует ли строка формату DD.MM.YYYY
    if len(date_str) == 10 and date_str[2] == '.' and date_str[5] == '.':
        try:
            return datetime.strptime(date_str, '%d.%m.%Y').date()
        except ValueError:
            # Если преобразование не удалось, возвращаем None
            print(f"Некорректная дата: {date_str}")
            return None
    # Проверяем, соответствует ли строка формату YYYY-MM-DD
    elif len(date_str) == 10 and date_str[4] == '-' and date_str[7] == '-':
        try:
            return datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            # Если преобразование не удалось, возвращаем None
            print(f"Некорректная дата: {date_str}")
            return None
    else:
        # Если формат не распознан, возвращаем None
        print(f"Некорректная дата: {date_str}")
        return None


# def convert_date(date_str):
#     """
#     Преобразует дату из формата DD.MM.YYYY в YYYY-MM-DD.
#     Если дата некорректна или пуста, возвращает None.
#     """
#     if not date_str:
#         return None
#     try:
#         return datetime.strptime(date_str, "%d.%m.%Y").date()
#     except ValueError:
#         print(f"Некорректная дата: {date_str}")
#         return None


def safe_float(value, default=0.0):
    if value is None:
        return default
    try:
        return float(value)
    except (ValueError, TypeError):
        return default
