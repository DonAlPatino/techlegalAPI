import asyncio
import logging
import sys
from pathlib import Path
from notifier import Notifier
from typing import Optional
from html import escape

from utils import escape_markdown


class TelegramLogHandler(logging.Handler):
    """Кастомный обработчик для Telegram с настраиваемым уровнем"""

    def __init__(self, notifier: Notifier, chat_id: int, min_level=logging.INFO):
        super().__init__(level=min_level)  # Устанавливаем минимальный уровень
        self.notifier = notifier
        self.chat_id = chat_id
        self.level_emojis = {
            logging.INFO: "ℹ️",
            logging.WARNING: "⚠️",
            logging.ERROR: "❌",
            logging.CRITICAL: "🔥"
        }
        self.formatter = logging.Formatter(
            fmt='%(levelname)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    def emit(self, record):
        try:
            emoji = self.level_emojis.get(record.levelno, "📌")
            msg = f"{emoji} {self.format(record)}"
            # Грязный хак для обработки HTML внутри телеги
            if "Ошибка декодирования JSON" in msg:
                safe_text = escape_markdown(msg)  # Было escape
                asyncio.run(self._send_msg(f"<pre>" + safe_text + "</pre>", parse_mode='Markdown'))
            else:
                asyncio.run(self._send_msg(f"<pre>" + msg + "</pre>"))
        except Exception as e:
            print(f"Telegram send failed: {e}")

    async def _send_msg(self, msg_text: str, parse_mode: Optional[str] = 'HTML'):
        """Внутренний метод для отправки сообщения"""
        async with self.notifier as notifier:
            await notifier.send_text(msg_text, self.chat_id, parse_mode)


def setup_logging(
        telegram_notifier: Optional[Notifier] = None,
        telegram_chat_id: Optional[int] = None,
        telegram_min_level: int = logging.INFO  # Новый параметр для уровня
):
    """Настройка логгера с гибкой интеграцией Telegram"""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Базовый форматтер
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Консоль (только INFO+)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Файл (все уровни)
    Path("logs").mkdir(exist_ok=True)
    file_handler = logging.FileHandler("logs/app.log", encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Обработчики
    # handlers = [console_handler, file_handler]
    # Set Only telegramm handler

    handlers = []
    # Telegram (если настроен)
    if telegram_notifier and telegram_chat_id:
        telegram_handler = TelegramLogHandler(
            notifier=telegram_notifier,
            chat_id=telegram_chat_id,
            min_level=telegram_min_level  # Передаем нужный уровень
        )
        handlers.append(telegram_handler)

    # Очистка старых обработчиков и добавление новых
    logger.handlers.clear()
    for handler in handlers:
        logger.addHandler(handler)

    return logger


# Пример инициализации
app_logger = setup_logging()
