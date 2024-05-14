import asyncio
from html import escape

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from app.main import redis


async def state_submitting_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    current_state,
):
    await redis.hset(
        update.effective_user.id,
        "submitting_message",
        update.effective_message.text,
    )

    await update.message.reply_text(
        escape("Твое сообщение:\n\n")
        + f"<b>{escape(await redis.hget(update.effective_user.id, 'submitting_message', encoding='utf-8', fallback='Нет сообщения'))}</b>\n",
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Сброс",
                        callback_data="reset",
                    ),
                    InlineKeyboardButton(
                        "Отправить",
                        callback_data="submit:message",
                    ),
                ]
            ]
        ),
    )


async def state_submitting_cafe(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    current_state,
):
    if current_state[2] == "name":

        await asyncio.gather(
            *[
                redis.hset(
                    update.effective_user.id,
                    "current_state",
                    "submitting:cafe:address",
                ),
                redis.hset(
                    update.effective_user.id,
                    "submitting_cafe_data:name",
                    update.effective_message.text,
                ),
            ]
        )

        await update.message.reply_text(
            "Теперь отправь мне адрес кофейни, "
            "которой тебе не хватает в нашем сервисе",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Сброс",
                            callback_data="reset",
                        )
                    ]
                ]
            ),
        )
    elif current_state[2] == "address":
        tasks = []
        tasks.append(
            redis.hset(
                update.effective_user.id,
                "submitting_cafe_data:address",
                update.effective_message.text,
            )
        )

        tasks.append(
            update.message.reply_text(
                escape("Твоя кофейня:\n\n")
                + f"<b>{escape((await redis.hget(update.effective_user.id,'submitting_cafe_data:name')).decode('utf-8'))}</b>\n"
                + f"<code>{escape((await redis.hget(update.effective_user.id,'submitting_cafe_data:address')).decode('utf-8'))}</code>",
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "Сброс",
                                callback_data="reset",
                            ),
                            InlineKeyboardButton(
                                "Отправить",
                                callback_data="submit:cafe",
                            ),
                        ]
                    ]
                ),
            )
        )
        await asyncio.gather(*tasks)


async def state_submitting(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    current_state,
):
    if current_state[1] == "cafe":
        await state_submitting_cafe(
            update, context, current_state
        )
    elif current_state[1] == "message":
        await state_submitting_message(
            update, context, current_state
        )
