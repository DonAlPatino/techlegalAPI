from decouple import config
from sqlalchemy import create_engine, Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base

db_user = config('DB_USER')
db_pass = config('DB_PASSWORD')
db_host = config('DB_HOST')
db_db = config('DB_DB')

DATABASE_URI = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:3306/{db_db}"

# Создаем базовый класс для моделей
Base = declarative_base()
def db_connect():
    # Подключаемся к базе данных
    engine = create_engine(DATABASE_URI)
    Base.metadata.create_all(engine)  # Создаем таблицу, если она не существует
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
