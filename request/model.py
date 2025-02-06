from datetime import datetime

from sqlalchemy import Column, Integer, String, Date, Float, func, Text, BIGINT
from sqlalchemy.orm import Mapped, mapped_column
from db import Base


# Модель для таблицы requests

class Request(Base):
    __tablename__ = 'techlegal_requests'
    id = Column(Integer, primary_key=True)
    epNumber = Column(String(50), nullable=True)
    requestName = Column(Text, nullable=False)
    collector = Column(String(255), nullable=False)
    debtor = Column(String(255), nullable=False)
    requestNumber = Column(String(50), nullable=True)
    requestDate = Column(Date, nullable=True)
    dateDocument = Column(Date, nullable=True)
    requestStatus = Column(String(100), nullable=True)
    isRequestInZip = Column(String(10), nullable=False)
    dateRequestInZip = Column(Date, nullable=True)
    responseDocName = Column(String(255), nullable=True)
    responseDocDate = Column(Date, nullable=True)
    ospName = Column(Text, nullable=True)
    responseText = Column(Text, nullable=True)
    textResolution = Column(Text, nullable=True)
    dateUpdate = Column(Date, nullable=True)
    caNumber = Column(String(255), nullable=False)
    userName = Column(String(512), nullable=False)
    requestIsAppeal = Column(String(255), nullable=True)
    edNumber = Column(String(128), nullable=True)
    edDate = Column(Date, nullable=True)
    idCreditFirm = Column(BIGINT, nullable=False, index=True)
    ca_dateStart = Column(Date, nullable=False)
    ca_dateEnd = Column(Date, nullable=True)
    rqSource = Column(String(100), nullable=False)
    credit_agreements_briefcase = Column(String(255), nullable=True)
    resSingName = Column(String(255), nullable=True)
    key = Column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())