from sqlalchemy import Column, Integer, String, Date, Float, Text, BIGINT
from model import BaseModel


# Модель для таблицы credits
class Credit(BaseModel):
    __tablename__ = 'techlegal_credits'
    credit_number = Column(String(255), nullable=False)
    credit_id = Column(BIGINT, nullable=True, index=True)
    debtor = Column(String(255), nullable=False)
    debtor_birthdate = Column(Date)
    osp_name = Column(String(500), nullable=True)
    ep_number = Column(String(255), nullable=True)
    ep_date_start = Column(Date, nullable=True)
    ep_date_end = Column(Date, nullable=True)
    ep_completion_basis = Column(String(255), nullable=True)
    ep_rest_debit = Column(Float)
    collector = Column(String(255))
    is_pension = Column(String(50))
    credit_status = Column(String(255))
    debtor_is_snils = Column(String(50))
    credit_date_start = Column(Date)
    credit_date_end = Column(Date, nullable=True)
    ep_status = Column(String(255), nullable=True)
    is_ep_confirmation = Column(String(50))
    responsible_user_fio = Column(String(255), nullable=True)
    date_fssp_request = Column(Date, nullable=True)
    ed_number = Column(String(128), nullable=True)
    ed_date = Column(Date, nullable=True)
    debtor_gender = Column(String(10))
    credit_agreements_suspended = Column(String(50))
    dtr_is_pasport = Column(String(50))
    receipts_before_input = Column(Integer)
    receipts_after_entering = Column(Integer)
    receipts_last_month = Column(Integer)

    # Добавка 05.05.25

    dateFamilMaterial = Column(String(10), nullable=True)  # дата ознакомления с материалами ИП
    chatLastMsg = Column(Text, nullable=True)  # последний комментарий
    chatLastMsgTime = Column(String(10), nullable=True)  # дата последнего комментария
    isPrimaryCollector = Column(String(64), nullable=True)  # Наличие первоочередного взыскателя
    amountPriorityAmount = Column(Float, nullable=True)  # Сумма первоочередных обязательств
    creditAuditTransfers = Column(String(64), nullable=True)  # Аудит перечислений
    ep_last_rest_debit = Column(Float, nullable=True)  # Остаток долга по ИП на дату (-30 дней)
    numberCase = Column(String(256), nullable=True)  # Дата и номер дела о банкротстве
    isSubsistenceMin = Column(String(256), nullable=True)  # Постановление ПМ
    edCompany_name = Column(String(256), nullable=True)  # Наименование организации (ФССП)
    epAppealCompany_name = Column(String(256), nullable=True)  # Название взыскателя ИД
    credit_agreements_briefcase_name = Column(String(256), nullable=True)  # Наименование портфеля
    debtor_inn_invalid_date = Column(String(5), nullable=True)  # Недействительный ИНН
    bailiff_executor_fio = Column(String(256), nullable=True)  # ФИО судебного пристава
    bailiff_executor_phone = Column(String(256), nullable=True)  # Телефон пристава
    dtr_inn = Column(String(64), nullable=True)  # ИНН должника
    note = Column(Text, nullable=True)  # Примечание
    yfssp_name = Column(Text, nullable=True)  # Наименование УФССАП
    edTp_name = Column(String(64), nullable=True)  # Тип Исполнительного документа
    dateRequestDeath = Column(String(10), nullable=True)  # Дата запроса ФНП
    dateDeath = Column(String(10), nullable=True)  # Дата смерти Должника
    inn_invalid_date = Column(String(10), nullable=True)  # Дата ИНН недействителен
    dateLastUpdateStatusCa = Column(String(10), nullable=True)  # Дата обновления статуса
    ep_rs_name = Column(String(64), nullable=True)  # ИП приостановлено