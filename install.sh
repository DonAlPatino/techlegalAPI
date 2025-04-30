#!/usr/bin/env bash

# Определение базовых переменных
CONFIG_FILE="./.env"
# Проверка существования файла
if [ -f "$CONFIG_FILE" ]; then
  source "$CONFIG_FILE"
else
  echo "Ошибка: файл конфигурации $CONFIG_FILE не найден." >&2
  exit 1
fi


# Создание БД
mysql -uroot -e "CREATE DATABASE $DB_NAME CHARACTER SET utf8 COLLATE utf8_general_ci" || {
  echo "Ошибка: не удалось создать базу данных $DB_NAME" >&2
  exit 1
}

mysql -uroot -e "CREATE USER $DB_USER@'127.0.0.1' IDENTIFIED BY '$DB_PASSWORD'" || {
  echo "Ошибка: не удалось создать пользователя $DB_USER" >&2
  exit 1
}

mysql -uroot -e "GRANT CREATE, SELECT, INSERT, UPDATE, INDEX, DELETE, ALTER ON $DB_NAME.* TO '$DB_USER'@'127.0.0.1'" || {
  echo "Ошибка: не удалось выдать права пользователю $DB_USER" >&2
  exit 1
}

# Переход в рабочую директорию
cd "${WORKDIR}" || {
  echo "Ошибка: не удалось перейти в директорию ${WORKDIR}" >&2
  exit 1
}

# Создание виртуального окружения, если оно еще не существует
if [ ! -d "${VENV_DIR}" ]; then
  python3 -m venv "${VENV_DIR}" || {
    echo "Ошибка: не удалось создать виртуальное окружение в ${VENV_DIR}" >&2
    exit 1
  }
fi

# Активация виртуального окружения
source "${VENV_DIR}/bin/activate" || {
  echo "Ошибка: не удалось активировать виртуальное окружение" >&2
  exit 1
}

# Установка зависимостей
pip install -r requirements.txt || {
  echo "Ошибка: не удалось установить зависимости" >&2
  exit 1
}