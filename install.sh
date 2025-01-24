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
mysql -uroot -e "CREATE DATABASE $DB CHARACTER SET utf8 COLLATE utf8_general_ci" || {
  echo "Ошибка: не удалось создать базу данных $DB" >&2
  exit 1
}

mysql -uroot -e "CREATE USER $USER@'127.0.0.1' IDENTIFIED BY '$PASS'" || {
  echo "Ошибка: не удалось создать пользователя $USER" >&2
  exit 1
}

mysql -uroot -e "GRANT SELECT, INSERT, UPDATE ON $DB.* TO '$USER'@'127.0.0.1'" || {
  echo "Ошибка: не удалось выдать права пользователю $USER" >&2
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