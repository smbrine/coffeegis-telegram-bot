from html import escape

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)
from telegram.constants import ParseMode
from telegram.ext import ContextTypes


async def state_submitting_cafe(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    current_state,
):
    if current_state[2] == "name":
        context.user_data["current_state"] = (
            "submitting:cafe:address"
        )
        context.user_data[
            "submitting_cafe_data"
        ] = {
            "name": update.effective_message.text
        }

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
        context.user_data["submitting_cafe_data"][
            "address"
        ] = update.effective_message.text
        await update.message.reply_text(
            escape("Твоя кофейня:\n\n")
            + f"<b>{escape(context.user_data['submitting_cafe_data']['name'])}</b>\n"
            + f"<code>{escape(context.user_data['submitting_cafe_data']['address'])}</code>",
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


async def state_submitting(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    current_state,
):
    if current_state[1] == "cafe":
        await state_submitting_cafe(
            update, context, current_state
        )
