from datetime import datetime
import requests
import asyncio

from telegram import send_msg


# Функция для выполнения запроса к API
def fetch_all_pages(base_url, token):
    data = {
        "token": token
    }
    all_results = []

    # Запрашиваем первую страницу
    response = requests.post(base_url, data=data)
    if response.status_code != 200:
        asyncio.run(send_msg(f"<pre>Ошибка при выполнении запроса {base_url}: {response.status_code} </pre>"))
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
            url = f"{base_url}/{page}"
            response = requests.post(url, data=data)
            if response.status_code == 200:
                page_data = response.json()
                all_results.extend(page_data.get("result", []))
            else:
                asyncio.run(send_msg(f"<pre>Ошибка при выполнении запроса для страницы {page}: {response.status_code} </pre>"))
                print(f"Ошибка при выполнении запроса для страницы {page}: {response.status_code}")

    return all_results


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
