from typing import Callable

from decouple import config
from sqlalchemy import create_engine, delete, MetaData, Table
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker, Session
from model import Base
from logs import LogRecord
from logs.model import Log
from utils import check_answer

# Настройка логирования
from log_config import app_logger

# Чтение переменных окружения со значениями по умолчанию
db_user = config('DB_USER', default='techlegal')
db_pass = config('DB_PASSWORD', default='default_password')
db_host = config('DB_HOST', default='localhost')
db_name = config('DB_NAME', default='techlegal')
records_per_page = int(config('RECORDS_PER_PAGE', default=5000))
store_days = int(config('STORE_DAYS', default=5))

DATABASE_URI = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:3306/{db_name}"


def delete_old_date(session: Session, table_name: str, store_day: int) -> Callable[[], int]:
    """
    Функция удаления старых данных.

    :param session: Сессия SQLAlchemy для работы с базой данных
    :param table_name: Название таблицы
    :param store_day: Кол-во дней, которые данные хранятся
    :return: Кол-во удаленных записей
    """
    # Создаем объект таблицы динамически
    metadata = MetaData()
    table = Table(table_name, metadata, autoload_with=session.bind)

    # Вычисляем дату, старше которой нужно удалить данные
    cutoff_date = datetime.now() - timedelta(days=store_day)
    # print(cutoff_date)
    # Формируем запрос на удаление
    stmt = delete(table).where(table.c.created_at < cutoff_date)
    # print(stmt)
    # Выполняем запрос
    result = session.execute(stmt)
    # print(result)
    # Фиксируем изменения в базе данных
    session.commit()

    # Возвращаем количество удаленных записей
    return result.rowcount


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
        app_logger.info(f"Данные успешно сохранены в таблицу {log_record.tablename}. Всего записей: {log_record.records}")
    except Exception as e:
        # В случае ошибки откатываем транзакцию и выводим сообщение об ошибке
        session.rollback()
        app_logger.error(f"Ошибка при сохранении данных в таблицу {log_record.tablename}: {e}")
    # Преобразуем LogRecord в объект SQLAlchemy
    sql_log_record = Log.from_pydantic(log_record)
    # Добавляем объект в сессию
    session.add(sql_log_record)

    try:
        # Пытаемся зафиксировать изменения в базе данных
        session.commit()
    except Exception as e:
        # В случае ошибки откатываем транзакцию и выводим сообщение об ошибке
        session.rollback()
        app_logger.error(f"Ошибка при сохранении данных в таблицу логов: {e}")
    if not check_answer(log_record.records, log_record.pages, records_per_page):
        app_logger.error(f"Неправильное кол-во страниц в {log_record.tablename}")

    # Удаление старых данных если не было ошибок при закачивании
    if log_record.has_error:
        return
    try:
        # Пытаемся зафиксировать изменения в базе данных
        deleted_count = delete_old_date(session, log_record.tablename, store_days)
        app_logger.info(f"Удалено записей из таблицы {log_record.tablename} : {deleted_count}")
    except Exception as e:
        # В случае ошибки откатываем транзакцию и выводим сообщение об ошибке
        session.rollback()
        app_logger.error(f"Ошибка при очистке данных в таблице {log_record.tablename}: {e}")
