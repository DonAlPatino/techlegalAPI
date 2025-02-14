from decouple import config
from sqlalchemy import create_engine, Column, Integer, String, Date, Float, ForeignKey, func
from datetime import datetime
from sqlalchemy.orm import sessionmaker, declarative_base
import asyncio
from model import Base
from logs import LogRecord
from logs.model import Log
from telegram import send_msg

db_user = config('DB_USER')
db_pass = config('DB_PASSWORD')
db_host = config('DB_HOST')
db_name = config('DB_NAME')

DATABASE_URI = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:3306/{db_name}"

def db_connect():
    # Подключаемся к базе данных
    engine = create_engine(DATABASE_URI)
    Base.metadata.create_all(engine)  # Создаем таблицу, если она не существует
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def save_to_database(session, log_record: LogRecord):
    """
        Функция для сохранения данных в базу данных с обработкой ошибок.

        :param log_record: LogRecord object
        :param session: SQLAlchemy сессия для работы с БД.
        """
    try:
        # Пытаемся зафиксировать изменения в базе данных
        session.commit()
        # Если commit выполнен успешно, отправляем сообщение и выводим информацию
        success_message = f"<pre>Данные успешно сохранены в таблицу {log_record.tablename}. Всего записей: {log_record.records}</pre>"
        print(f"Данные успешно сохранены в таблицу {log_record.tablename}. Всего записей: {log_record.records}")
        asyncio.run(send_msg(success_message))
    except Exception as e:
        # В случае ошибки откатываем транзакцию и выводим сообщение об ошибке
        session.rollback()
        error_message = f"Ошибка при сохранении данных в таблицу {log_record.tablename}: {e}"
        print(error_message)
        asyncio.run(send_msg(f"<pre>Ошибка при сохранении данных в таблицу techlegal_credit:{error_message}</pre>"))

    # Преобразуем LogRecord в объект SQLAlchemy
    sql_log_record = Log.from_pydantic(log_record)
    # Добавляем объект в сессию
    session.add(sql_log_record)
    # Сохраняем изменения в базе данных
    session.commit()
