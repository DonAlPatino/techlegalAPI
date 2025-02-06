from datetime import datetime

from sqlalchemy import Column, Integer, String, Date, Float, func, Text, BIGINT
from sqlalchemy.orm import Mapped, mapped_column
from db import Base


# Модель для таблицы subject

class Subject(Base):
    __tablename__ = 'techlegal_subjects'
    id = Column(Integer, primary_key=True)
    debtor = Column(String(255), nullable=False)
    subjectType = Column(String(255), nullable=True)
    subjectInfo = Column(Text, nullable=True)
    epAmountOwed = Column(Float, nullable=True)
    epRestDebit = Column(Float, nullable=True)
    epNumber = Column(String(128), nullable=True)
    epDateStart = Column(Date, nullable=True)
    ospName = Column(Text, nullable=True)
    collector = Column(String(512), nullable=False)
    worthInCashAccount = Column(Float, nullable=True)
    subjectMeasureName = Column(Text, nullable=True)
    subjectMeasureDate = Column(Date, nullable=True)
    # не по спеке
    dateRelevant = Column(Date, nullable=True)
    caNumber = Column(String(256), nullable=False)
    # не по спеке
    ca_dateStart = Column(Date, nullable=True)
    ca_dateEnd = Column(Date, nullable=True)
    responsibleUser_fio = Column(String(512), nullable=False)
    idCreditFirm = Column(BIGINT, nullable=True, index=True)
    edNumber = Column(String(128), nullable=True)
    edDate = Column(Date, nullable=True)
    caStatus = Column(String(100), nullable=False)
    requestDate = Column(Date, nullable=True)
    numberGD = Column(String(100), nullable=True)
    dateGD = Column(Date, nullable=True)
    credit_agreements_briefcase = Column(String(255), nullable=True)
    creditId = Column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())