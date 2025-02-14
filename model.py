from sqlalchemy import create_engine, Column, Integer, String, Date, Float, ForeignKey, func
from datetime import datetime
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm import Mapped, mapped_column

# Создаем базовый класс для моделей
Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True  # Указываем, что это абстрактный класс, и он не будет создавать таблицу в БД
    id = Column(Integer, primary_key=True, autoincrement=True)  # Уникальный идентификатор
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())  # Дата и время создания записи
    slice_tag = Column(String(25), nullable=True, index=True)