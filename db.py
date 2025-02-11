from decouple import config
from sqlalchemy import create_engine, Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base
import asyncio
from telegram import send_msg

db_user = config('DB_USER')
db_pass = config('DB_PASSWORD')
db_host = config('DB_HOST')
db_name = config('DB_NAME')

DATABASE_URI = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:3306/{db_name}"

# Создаем базовый класс для моделей
Base = declarative_base()


def db_connect():
    # Подключаемся к базе данных
    engine = create_engine(DATABASE_URI)
    Base.metadata.create_all(engine)  # Создаем таблицу, если она не существует
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def save_to_database(session, num_of_results, table_name):
    """
        Функция для сохранения данных в базу данных с обработкой ошибок.

        :param session: SQLAlchemy сессия для работы с БД.
        :param num_of_results: Данные, которые были сохранены (для подсчета количества записей).
        :param table_name: Название таблицы, куда сохраняются данные.
        """
    try:
        # Пытаемся зафиксировать изменения в базе данных
        session.commit()
        # Если commit выполнен успешно, отправляем сообщение и выводим информацию
        success_message = f"<pre>Данные успешно сохранены в таблицу {table_name}. Всего записей: {num_of_results}</pre>"
        print(f"Данные успешно сохранены в таблицу {table_name}. Всего записей: {num_of_results}")
        asyncio.run(send_msg(success_message))
    except Exception as e:
        # В случае ошибки откатываем транзакцию и выводим сообщение об ошибке
        session.rollback()
        error_message = f"Ошибка при сохранении данных в таблицу {table_name}: {e}"
        print(error_message)
        asyncio.run(send_msg(f"<pre>Ошибка при сохранении данных в таблицу techlegal_credit:{error_message}</pre>"))
