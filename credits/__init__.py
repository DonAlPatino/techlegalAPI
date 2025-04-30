from pympler import asizeof
from logs import LogRecord
from utils import convert_date, safe_float
from credits.model import Credit


# Функция для выполнения запроса к API
def saveCredit2db(results, session, log_record: LogRecord):
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
            slice_tag=log_record.slice_tag,

            # Добавка 05.05.25

            dateFamilMaterial=item.get("dateFamilMaterial"),
            chatLastMsg=item.get("chatLastMsg"),
            chatLastMsgTime=item.get("chatLastMsgTime"),
            isPrimaryCollector=item.get("isPrimaryCollector"),
            amountPriorityAmount=safe_float(item.get("amountPriorityAmount")),
            creditAuditTransfers=item.get("creditAuditTransfers"),
            ep_last_rest_debit=safe_float(item.get("epLastRestDebit")),
            numberCase=item.get("numberCase"),
            isSubsistenceMin=item.get("isSubsistenceMin"),
            edCompany_name=item.get("edCompanyName"),
            epAppealCompany_name=item.get("epAppealCompanyName"),
            credit_agreements_briefcase_name=item.get("creditAgreementsBriefcaseName"),
            debtor_inn_invalid_date=item.get("debtorInnInvalidDate"),
            bailiff_executor_fio=item.get("bailiffExecutorFio"),
            bailiff_executor_phone=item.get("bailiffExecutorPhone"),
            dtr_inn=item.get("dtrInn"),
            note=item.get("note"),
            yfssp_name=item.get("yfsspName"),
            edTp_name=item.get("edTpName"),
            dateRequestDeath=item.get("dateRequestDeath"),
            dateDeath=item.get("dateDeath"),
            inn_invalid_date=item.get("innInvalidDate"),
            dateLastUpdateStatusCa=item.get("dateLastUpdateStatusCa"),
            ep_rs_name=item.get("epRsName"),
        )
        session.add(credit)

    return asizeof.asizeof(results)




