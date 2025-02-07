import os
from decouple import config
from easy_async_tg_notify import Notifier


token = config('TELEGRAM_BOT_TOKEN')
user_id = int(config('TELEGRAM_CHAT_ID'))
users_ids = [int(id) for id in config('TELEGRAM_CHAT_IDS').split(',')]

script_dir = os.path.dirname(os.path.abspath(__file__))
#photo = os.path.join(script_dir, 'telegram-logo-27.png')

async def send_msg(msg_text: str):
    async with Notifier(token) as notifier:
        await notifier.send_text(msg_text, users_ids[1])