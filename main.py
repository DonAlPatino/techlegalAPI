from decouple import config

from credits import fetch_all_pages
from credits.model import Credit
from db import db_connect
from utils import convert_date

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

    # Сохраняем данные в БД
    for item in results:
        credit = Credit(
            credit_number=item.get("creditNumber"),
            credit_id=item.get("creditId"),
            debtor=item.get("debtor"),
            debtor_birthdate=convert_date(item.get("debtorBirthdate")),  # Преобразуем дату
            osp_name=item.get("ospName"),
            ep_number=item.get("epNumber"),
            ep_date_start=convert_date(item.get("epDateStart")),  # Преобразуем дату
            ep_date_end=convert_date(item.get("epDateEnd")),  # Преобразуем дату
            ep_completion_basis=item.get("epCompletionBasis"),
            ep_rest_debit=item.get("epRestDebit"),
            collector=item.get("collector"),
            is_pension=item.get("isPension"),
            credit_status=item.get("creditStatus"),
            debtor_is_snils=item.get("debtorIsSnils"),
            credit_date_start=convert_date(item.get("creditDateStart")),  # Преобразуем дату
            credit_date_end=convert_date(item.get("creditDateEnd")),  # Преобразуем дату
            ep_status=item.get("epStatus"),
            is_ep_confirmation=item.get("isEpСonfirmation"),
            responsible_user_fio=item.get("responsibleUser_fio"),
            date_fssp_request=convert_date(item.get("dateFsspRequest")),  # Преобразуем дату
            ed_number=item.get("ed_number"),
            ed_date=convert_date(item.get("edDate")),  # Преобразуем дату
            debtor_gender=item.get("debtorGender"),
            credit_agreements_suspended=item.get("credit_agreements_suspended"),
            dtr_is_pasport=item.get("dtr_is_pasport"),
            receipts_before_input=item.get("receiptsBeforeInput"),
            receipts_after_entering=item.get("receiptsAfterEntering"),
            receipts_last_month=item.get("receiptsLastMonth"),
        )
        session.add(credit)

    # Сохраняем изменения в БД
    session.commit()
    print(f"Данные успешно сохранены в БД. Всего записей: {len(results)}")


if __name__ == "__main__":
    main()
