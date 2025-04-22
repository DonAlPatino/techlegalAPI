from pympler import asizeof

from db import save_to_database
from logs import LogRecord
from request.model import Request
from utils import convert_date


# Функция для выполнения запроса к API
def saveRequest2db(results, session, log_record: LogRecord):
    # Сохраняем данные в БД
    for item in results:
        request = Request(
            epNumber=item.get('epNumber'),
            requestName=item.get('requestName'),
            collector=item.get('collector'),
            debtor=item.get('debtor'),
            requestNumber=item.get('requestNumber'),
            requestDate=convert_date(item.get('requestDate')),
            dateDocument=convert_date(item.get('dateDocument')),
            requestStatus=item.get('requestStatus'),
            isRequestInZip=item.get('isRequestInZip'),
            dateRequestInZip=convert_date(item.get('dateRequestInZip')),
            responseDocName=item.get('responseDocName'),
            responseDocDate=convert_date(item.get('responseDocDate')),
            ospName=item.get('ospName'),
            responseText=item.get('responseText'),
            textResolution=item.get('textResolution'),
            dateUpdate=convert_date(item.get('dateUpdate')),
            caNumber=item.get('caNumber'),
            userName=item.get('userName'),
            requestIsAppeal=item.get('requestIsAppeal'),
            edNumber=item.get('edNumber'),
            edDate=convert_date(item.get('edDate')),
            idCreditFirm=item.get('idCreditFirm'),
            ca_dateStart=convert_date(item.get('ca_dateStart')),
            ca_dateEnd=convert_date(item.get('ca_dateEnd')),
            rqSource=item.get('rqSource'),
            credit_agreements_briefcase=item.get('credit_agreements_briefcase'),
            resSingName=item.get('resSingName'),
            key=item.get('key'),
            slice_tag=log_record.slice_tag
        )
        session.add(request)
    return asizeof.asizeof(results)
