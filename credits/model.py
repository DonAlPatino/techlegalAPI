from sqlalchemy import Column, Integer, String, Date, Float, func, BIGINT
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
