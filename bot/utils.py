from telegram import Bot
from telegram.constants import ParseMode


async def notify_administrators(
    bot: Bot,
    admin_chat_id: int,
    payload: dict | str,
):
    await bot.send_message(
        admin_chat_id,
        payload,
        parse_mode=ParseMode.HTML,
    )
