import asyncio

from db import save_to_database
from logs import LogRecord
from subject.model import Subject
from telegram import send_msg
from utils import convert_date, safe_float


# Функция для выполнения запроса к API

def saveSubject2db(results, session, log_record: LogRecord):
    # Сохраняем данные в БД
    for item in results:
        subject = Subject(
            debtor=item.get('debtor'),
            subjectType=item.get('subjectType'),
            subjectInfo=item.get('subjectInfo'),
            epAmountOwed=safe_float(item.get('epAmountOwed', 0)),
            epRestDebit=safe_float(item.get('epRestDebit', 0)),
            epNumber=item.get('epNumber'),
            epDateStart=convert_date(item.get('epDateStart')),
            ospName=item.get('ospName'),
            collector=item.get('collector'),
            worthInCashAccount=safe_float(item.get('worthInCashAccount', 0)),
            subjectMeasureName=item.get('subjectMeasureName'),
            subjectMeasureDate=convert_date(item.get('subjectMeasureDate')),
            dateRelevant=convert_date(item.get('dateRelevant')),
            caNumber=item.get('caNumber'),
            ca_dateStart=convert_date(item.get('ca_dateStart')),
            ca_dateEnd=convert_date(item.get('ca_dateEnd')),
            responsibleUser_fio=item.get('responsibleUser_fio'),
            idCreditFirm=item.get('idCreditFirm'),
            edNumber=item.get('edNumber'),
            edDate=convert_date(item.get('edDate')),
            caStatus=item.get('caStatus'),
            requestDate=convert_date(item.get('requestDate')),
            numberGD=item.get('numberGD'),
            dateGD=convert_date(item.get('dateGD')),
            credit_agreements_briefcase=item.get('credit_agreements_briefcase'),
            creditId=item.get('creditId'),
            slice_tag=log_record.slice_tag
        )
        session.add(subject)
    # Сохраняем изменения в БД
    log_record.tablename = "techlegal_subject"
    save_to_database(session, log_record)
