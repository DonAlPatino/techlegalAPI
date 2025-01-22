from decouple import config

from credits import saveCredit2db
from db import db_connect
from utils import fetch_all_pages

tg_token = config('TELEGRAM_BOT_TOKEN')
user_id = int(config('TELEGRAM_CHAT_ID'))
users_ids = [int(id) for id in config('TELEGRAM_CHAT_IDS').split(',')]

base_url = config('BASE_CREDIT_URL')
token = config('TOKEN')


# Основная функция
def main():
    session = db_connect()
    # Получаем данные из API
    results = fetch_all_pages(base_url, token)
    if not results:
        print("Не удалось получить данные.")
        return

    saveCredit2db(results, session)


if __name__ == "__main__":
    main()
