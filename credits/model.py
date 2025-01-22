from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey

# Создаем базовый класс для моделей
Base = declarative_base()


# Модель для таблицы credits
class Credit(Base):
    __tablename__ = 'credits'

    id = Column(Integer, primary_key=True, autoincrement=True)
    credit_number = Column(String(50), nullable=False)
    credit_id = Column(String(50), nullable=False)
    debtor = Column(String(255), nullable=False)
    debtor_birthdate = Column(Date)
    osp_name = Column(String(500))
    ep_number = Column(String(255))
    ep_date_start = Column(Date)
    ep_date_end = Column(Date)
    ep_completion_basis = Column(String(255))
    ep_rest_debit = Column(Float)
    collector = Column(String(255))
    is_pension = Column(String(50))
    credit_status = Column(String(255))
    debtor_is_snils = Column(String(50))
    credit_date_start = Column(Date)
    credit_date_end = Column(Date)
    ep_status = Column(String(255))
    is_ep_confirmation = Column(String(50))
    responsible_user_fio = Column(String(255))
    date_fssp_request = Column(Date)
    ed_number = Column(String(255))
    ed_date = Column(Date)
    debtor_gender = Column(String(10))
    credit_agreements_suspended = Column(String(50))
    dtr_is_pasport = Column(String(50))
    receipts_before_input = Column(Integer)
    receipts_after_entering = Column(Integer)
    receipts_last_month = Column(Integer)