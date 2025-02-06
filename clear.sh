#!/usr/bin/env bash

# Определение базовых переменных
WORKDIR="/srv/db/techlegal"
# Переход в рабочую директорию
cd "${WORKDIR}" || {
  echo "Ошибка: не удалось перейти в директорию ${WORKDIR}" >&2
  exit 1
}

# Определение базовых переменных
CONFIG_FILE="./.env"
# Проверка существования файла
if [ -f "$CONFIG_FILE" ]; then
  source "$CONFIG_FILE"
else
  echo "Ошибка: файл конфигурации $CONFIG_FILE не найден." >&2
  exit 1
fi

mysql -u"$DB_USER" -p"$DB_PASSWORD" -h"$DB_HOST" "$DB_NAME" < "$SQL_SCRIPT" > "$LOG_FILE" 2>&1