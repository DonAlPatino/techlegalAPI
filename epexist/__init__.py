from pympler import asizeof
from epexist.model import Epexist
from logs import LogRecord
from utils import safe_float


# Функция для выполнения запроса к API
def saveEpexist2db(results, session, log_record: LogRecord):
    # Сохраняем данные в БД
    for item in results:
        epexist = Epexist(
            debtor=item.get('debtor'),
            debtor_birthdate=item.get('debtorBirthdate'),
            debtor_inn=item.get('debtorInn'),
            osp_name=item.get('ospName'),
            spi_short_name=item.get('SPIShortName'),
            ep_number=item.get('epNumber'),
            ep_date_start=item.get('epDateStart'),
            ep_status=item.get('epStatus'),
            ep_date_end=item.get('epDateEnd'),
            ep_completion_basis=item.get('epCompletionBasis'),
            ep_rest_debit=safe_float(item.get('epRestDebit'), 0),
            ep_subject_execution=item.get('ep_subject_execution'),
            number_cd=item.get('number_cd'),
            ed_number=item.get('edNumber'),
            ed_date=item.get('edDate'),
            ed_issuing_authority=item.get('ed_issuing_authority'),
            ed_company_name=item.get('edCompany_name'),
            ed_company_inn=item.get('edCompany_inn'),
            collector=item.get('collector'),
            collector_inn=item.get('collectorInn'),
            date_fssp_request=item.get('dateFsspRequest'),
            request_date=item.get('requestDate'),
            date_document=item.get('dateDocument'),
            request_status=item.get('requestStatus'),
            is_request_in_zip=item.get('isRequestInZip'),
            date_request_in_zip=item.get('dateRequestInZip'),
            response_doc_name=item.get('responseDocName'),
            response_doc_date=item.get('responseDocDate'),
            slice_tag=log_record.slice_tag
        )
        session.add(epexist)
    print(f"EPEXIST size: {asizeof.asizeof(results) / (1024 * 1024):.2f} MB")
