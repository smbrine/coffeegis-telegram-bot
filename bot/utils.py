from telegram import Bot
from telegram.constants import ParseMode

from app import settings


async def notify_administrators(
    bot: Bot,
    payload: dict | str,
):
    await bot.send_message(
        settings.ADMIN_CHAT_ID,
        payload,
        parse_mode=ParseMode.HTML,
    )
