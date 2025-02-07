import asyncio

from telegram import send_msg
from utils import convert_date, safe_float
from credits.model import Credit


# Функция для выполнения запроса к API
def saveCredit2db(results, session):
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
            ep_rest_debit=safe_float(item.get('epRestDebit', 0)),
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
    asyncio.run(send_msg(f"<pre>Данные успешно сохранены в таблицу techlegal_subjects. Всего записей: {len(results)} </pre>"))
    print(f"Данные успешно сохранены в таблицу tachlegal_credit. Всего записей: {len(results)}")
