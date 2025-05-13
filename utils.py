from datetime import datetime
import random
import string


def escape_markdown(text):
    """
    Экранирует специальные символы Markdown в тексте.
    """
    escape_chars = ['\\', '_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '!']
    for char in escape_chars:
        text = text.replace(char, f'\\{char}')
    return text


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

    #   return lower_bound <= records <= upper_bound
    return lower_bound < records < upper_bound


def generate_random_label(length=8):
    characters = string.ascii_letters + string.digits  # Используем буквы и цифры
    random_label = ''.join(random.choice(characters) for _ in range(length))
    return random_label


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
