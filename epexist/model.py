from sqlalchemy import Column, Integer, String, Date, Float, func, Text, BIGINT
from model import BaseModel


# Модель для таблицы epexist

class Epexist(BaseModel):
    __tablename__ = 'techlegal_epexist'

    id = Column(Integer, primary_key=True)
    debtor = Column(String(255), nullable=True)  # ФИО должника
    debtor_birthdate = Column(String(10), nullable=True)  # Дата рождения (DD.MM.YYYY)
    debtor_inn = Column(String(64), nullable=True)  # ИНН должника
    osp_name = Column(String(255), nullable=True)  # Наименование ОСП
    spi_short_name = Column(String(255), nullable=True)  # ФИО пристава-исполнителя
    ep_number = Column(String(128), nullable=True)  # Номер ИП
    ep_date_start = Column(String(10), nullable=True)  # Дата возбуждения (DD.MM.YYYY)
    ep_status = Column(String(10), nullable=True)  # Активен/Завершен
    ep_date_end = Column(String(10), nullable=True)  # Дата окончания (DD.MM.YYYY)
    ep_completion_basis = Column(String(64), nullable=True)  # Основание завершения
    ep_rest_debit = Column(Float, nullable=True)  # Остаток задолженности
    ep_subject_execution = Column(String(255), nullable=True)  # Вид исполнения
    number_cd = Column(String(128), nullable=True)  # Номер СД
    ed_number = Column(String(128), nullable=True)  # Номер исполнительного документа
    ed_date = Column(String(10), nullable=True)  # Дата ИД (DD.MM.YYYY)
    ed_issuing_authority = Column(String(255), nullable=True)  # Суд
    ed_company_name = Column(String(256), nullable=True)  # Наименование организации
    ed_company_inn = Column(String(64), nullable=True)  # ИНН организации
    collector = Column(String(512), nullable=True)  # Взыскатель
    collector_inn = Column(String(64), nullable=True)  # ИНН взыскателя
    date_fssp_request = Column(String(10), nullable=True)  # Дата запроса в ФССП
    request_date = Column(String(10), nullable=True)  # Дата обращения на ЕПГУ
    date_document = Column(String(10), nullable=True)  # Дата формирования обращения
    request_status = Column(String(128), nullable=True)  # Статус обращения
    is_request_in_zip = Column(String(5), nullable=True)  # В архиве (да/нет)
    date_request_in_zip = Column(String(10), nullable=True)  # Дата архивации
    response_doc_name = Column(String(255), nullable=True)  # Ответ на обращение
    response_doc_date = Column(String(10), nullable=True)  # Дата ответа

