import asyncio
import base64
import json
import pickle
from html import escape

import telegram
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
from app.main import redis
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
                await redis.hget(
                    update.effective_user.id,
                    "submitting_cafe_data:name",
                )
            ):
                return
            contents = {
                "name": await redis.hget(
                    update.effective_user.id,
                    "submitting_cafe_data:name",
                    encoding="utf-8",
                ),
                "address": await redis.hget(
                    update.effective_user.id,
                    "submitting_cafe_data:address",
                    encoding="utf-8",
                ),
            }
            await redis.hset(
                update.effective_user.id,
                "current_state",
                "",
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
        case "message":
            tasks = []
            if not (
                message := await redis.hget(
                    update.effective_user.id,
                    "submitting_message",
                    encoding="utf-8",
                )
            ):
                return
            contents = {
                "message": message,
            }
            await redis.hset(
                update.effective_user.id,
                "current_state",
                "",
            )

            async with (
                sessionmanager.session() as session
            ):
                tasks.append(
                    models.Request.create(
                        session,
                        author_telegram_id=update.effective_user.id,
                        request_type="message",
                        contents=contents,
                    )
                )
            tasks.append(
                notify_administrators(
                    bot,
                    escape(
                        f"@{update.effective_user.username} submitted message:\n\n"
                    )
                    + f'<pre language="json">{json.dumps(contents, ensure_ascii=False, indent=4)}</pre>',
                )
            )
            msg = "Сообщение передано администраторам. Спасибо, что делаете нашего бота лучше!"
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

    cafes = json.loads(
        await redis.hget(
            query.from_user.id,
            "cafes",
            encoding="utf-8",
            fallback="[]",
        )
    )
    if not cafes:
        error_msg = "Произошла ошибка. Попробуй начать с команды /start"
        try:
            await query.edit_message_text(
                error_msg,
            )
        except telegram.error.BadRequest:
            await bot.send_message(
                query.from_user.id, error_msg
            )
        return

    cafes_coords = json.loads(
        await redis.hget(
            query.from_user.id,
            "cafes_coords",
            encoding="utf-8",
        )
    )
    cafes_images = json.loads(
        await redis.hget(
            query.from_user.id, "cafes_images"
        )
    )
    current_index = int(
        await redis.hget(
            query.from_user.id,
            "selected_cafe",
            encoding="utf-8",
            fallback=0,
        )
    )
    if len(cafes) == 1:
        return

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
        await redis.hset(
            query.from_user.id, "selected_cafe", 0
        )
        keyboard = (
            await keyboards.get_cafe_card_buttons(
                1,
                len(cafes),
                cafes[0].get("latitude"),
                cafes[0].get("longitude"),
            )
        )
        next_index = 0
        await query.edit_message_caption(
            cafes[0],
            parse_mode=ParseMode.HTML,
            reply_markup=keyboard,
        )
        await query.edit_message_media(
            pickle.loads(
                base64.b64decode(cafes_images[0])
            )
        )

    await redis.hset(
        query.from_user.id,
        "selected_cafe",
        next_index,
    )
    keyboard = (
        await keyboards.get_cafe_card_buttons(
            next_index + 1,
            len(cafes),
            cafes_coords[next_index].get(
                "latitude"
            ),
            cafes_coords[next_index].get(
                "longitude"
            ),
        )
    )
    media = pickle.loads(
        base64.b64decode(cafes_images[next_index])
    )
    await query.delete_message()
    await bot.send_photo(
        query.from_user.id,
        media,
        cafes[next_index],
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard,
        disable_notification=True,
    )
    # await query.edit_message_media(
    #     media
    # )
    # await query.edit_message_caption(
    #     cafes[next_index],
    #     parse_mode=ParseMode.HTML,
    #     reply_markup=keyboard,
    # )


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


async def callback_reset(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    tasks = []
    user_id = update.effective_user.id
    msg = "Отправь мне свою геопозицию и я подскажу где неподалёку есть кофейни из нашей подборки!"

    async with (
        sessionmanager.session() as session
    ):
        if not (
            user_profile := await models.Profile.get_by_telegram_id(
                session,
                user_id,
            )
        ):
            await models.Profile.create(
                session,
                user_telegram_id=user_id,
            )
            user_profile = await models.Profile.get_by_telegram_id(
                session,
                user_id,
            )

        is_phone_confirmed = (
            user_profile.is_phone_confirmed
        )

    keyboard = await keyboards.get_start_keyboard(
        is_phone_confirmed
    )
    await asyncio.gather(
        *[
            redis.hset(
                user_id, "current_state", "start"
            ),
            update.callback_query.delete_message(),
            update.effective_message.reply_text(
                msg, reply_markup=keyboard
            ),
        ]
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
            await callback_reset(update, context)
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
