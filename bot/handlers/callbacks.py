import asyncio
import json
from html import escape

from telegram import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from telegram.ext._utils.types import CCT

from app import settings
from bot import keyboards, handlers
from bot.utils import notify_administrators
from db import models
from db.main import sessionmanager
from bot.main import bot


async def callback_submit(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    match update.callback_query.data.split(":")[
        1
    ]:
        case "cafe":
            tasks = []
            if not (
                submitting_cafe_data := context.user_data.get(
                    "submitting_cafe_data"
                )
            ):
                return
            contents = {
                "name": submitting_cafe_data[
                    "name"
                ],
                "address": submitting_cafe_data[
                    "address"
                ],
            }
            context.user_data["current_state"] = (
                ""
            )
            async with (
                sessionmanager.session() as session
            ):
                tasks.append(
                    models.Request.create(
                        session,
                        author_telegram_id=update.effective_user.id,
                        request_type="cafe",
                        contents=contents,
                    )
                )
            tasks.append(
                notify_administrators(
                    bot,
                    settings.ADMIN_CHAT_ID,
                    escape(
                        f"@{update.effective_user.username} submitted cafe:\n\n"
                    )
                    + f'<pre language="json">{json.dumps(contents, ensure_ascii=False, indent=4)}</pre>',
                )
            )
            msg = "Кофейня передана администраторам. Спасибо, что делаете нашего бота лучше!"
            tasks.append(
                update.callback_query.edit_message_text(
                    msg,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    text="Домой",
                                    callback_data="reset",
                                )
                            ]
                        ],
                    ),
                )
            )
            await asyncio.gather(*tasks)
        case _:
            pass


async def callback_scroll(
    query: CallbackQuery,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:

    direction = query.data.split(":")[1]

    if direction == "pass":
        return
    cafes = context.user_data.get("cafes")
    if not cafes:
        await query.edit_message_text(
            "Произошла ошибка. Попробуй начать с команды /start",
        )
        return
    current_index = context.user_data.get(
        "selected_cafe", 0
    )
    if direction == "backwards":
        next_index = (
            current_index - 1
            if current_index > 0
            else len(cafes) - 1
        )
    elif direction == "forward":
        next_index = (
            current_index + 1
            if current_index < len(cafes) - 1
            else 0
        )
    else:
        context.user_data["selected_cafe"] = 0
        keyboard = (
            await keyboards.get_cafe_card_buttons(
                1,
                len(context.user_data["cafes"]),
                context.user_data["cafes"][0].get(
                    "latitude"
                ),
                context.user_data["cafes"][0].get(
                    "longitude"
                ),
            )
        )
        next_index = 0
        await query.edit_message_text(
            context.user_data["cafes"][0],
            parse_mode=ParseMode.HTML,
            reply_markup=keyboard,
        )

    context.user_data["selected_cafe"] = (
        next_index
    )
    keyboard = (
        await keyboards.get_cafe_card_buttons(
            next_index + 1,
            len(cafes),
            context.user_data["cafes_coords"][
                next_index
            ].get("latitude"),
            context.user_data["cafes_coords"][
                next_index
            ].get("longitude"),
        )
    )

    await query.edit_message_text(
        cafes[next_index],
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard,
    )


async def callback_inline(
    query: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    lat = float(
        query.callback_query.data.split(":")[3]
    )
    lon = float(
        query.callback_query.data.split(":")[4]
    )

    await query.callback_query.edit_message_live_location(
        lat, lon
    )


async def callback_send(
    query: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    lat = float(
        query.callback_query.data.split(":")[2]
    )
    lon = float(
        query.callback_query.data.split(":")[3]
    )

    await query.effective_chat.send_location(
        lat, lon
    )


async def callback_any(
    update: Update, context: CCT
) -> None:
    query = update.callback_query

    main_callback = query.data.split(":")[0]
    await query.answer()
    match main_callback:
        case "switch":
            await callback_scroll(query, context)
        case "reset":
            await handlers.command_start(
                update, context
            )
        case "submit":
            await callback_submit(update, context)
        case "inline":
            await callback_inline(update, context)
        case "send":
            await callback_send(update, context)
        case _:
            await query.edit_message_text(
                "Ошибка. Перезапусти бота при помощи команды /start",
            )
