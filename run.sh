#!/usr/bin/env bash

# Настройка строгого режима выполнения скрипта
set -euo pipefail

# Определение базовых переменных
WORKDIR="/srv/db/techlegal"
VENV_DIR="${WORKDIR}/venv"
PYTHON_SCRIPT="main.py"
# Переход в рабочую директорию
cd "${WORKDIR}" || {
  echo "Ошибка: не удалось перейти в директорию ${WORKDIR}" >&2
  exit 1
}

# Активация виртуального окружения
if [[ -f "${VENV_DIR}/bin/activate" ]]; then
  source "${VENV_DIR}/bin/activate"
else
  echo "Ошибка: виртуальное окружение не найдено в ${VENV_DIR}" >&2
  exit 1
fi

# Запуск Python-скрипта
if [[ -f "${PYTHON_SCRIPT}" ]]; then
  python3 "${PYTHON_SCRIPT}"
else
  echo "Ошибка: файл ${PYTHON_SCRIPT} не найден" >&2
  exit 1
fi
