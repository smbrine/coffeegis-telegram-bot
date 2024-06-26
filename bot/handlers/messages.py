import asyncio
import base64
import json
import pickle

import grpc
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    Update,
)
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from app.main import redis

from bot import handlers, keyboards
from bot.main import pb, img_svc
from bot import generators
from db import models
from db.main import sessionmanager


async def message_location(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    async with (
        sessionmanager.session() as session
    ):
        user_profile = await models.Profile.get_by_telegram_id(
            session, update.effective_user.id
        )
        await user_profile.increment_general_requests(
            session
        )
    amount_of_cafes = 50
    response = await pb.ListCafesPerCity(
        update.message.location.latitude,
        update.message.location.longitude,
        amount_of_cafes,
        bypass_cache=user_profile.is_admin,
    )

    cafes = []

    cafes_coords = []
    cafes_images = []
    raw_cafes = []
    search_distance = (
        user_profile.preferences.max_search_distance
        or 5
    )

    if (
        response.cafes[4].distance
        < search_distance
    ):
        for cafe in response.cafes:
            if (
                not cafe.distance
                <= search_distance
            ):
                break
            raw_cafes.append(cafe)
    else:
        raw_cafes = response.cafes[:5]

    # TODO: send placeholder if no cafes in response
    for cafe in raw_cafes[:10]:

        serialized_cafe = (
            await generators.generate_cafe_card(
                cafe
            )
        )

        cafes.append(serialized_cafe)

        cafes_coords.append(
            {
                "latitude": cafe.latitude,
                "longitude": cafe.longitude,
            }
        )
        try:
            image_bytes = (
                await img_svc.GetImage(
                    cafe.description.image_uuid
                )
            ).content

        except grpc.aio._call.AioRpcError as e:
            image_bytes = open(
                "./data/default.webp",
                "rb",
            ).read()

        image = base64.b64encode(
            pickle.dumps(image_bytes)
        ).decode("utf-8")

        cafes_images.append(image)

    await asyncio.gather(
        *[
            redis.hset(
                update.effective_user.id,
                "cafes",
                json.dumps(
                    cafes, ensure_ascii=False
                ),
            ),
            redis.hset(
                update.effective_user.id,
                "cafes_coords",
                json.dumps(
                    cafes_coords,
                    ensure_ascii=False,
                ),
            ),
            redis.hset(
                update.effective_user.id,
                "cafes_images",
                json.dumps(
                    cafes_images,
                    ensure_ascii=False,
                ),
            ),
            redis.hset(
                update.effective_user.id,
                "selected_cafe",
                0,
            ),
        ]
    )

    cafes_coords = json.loads(
        await redis.hget(
            update.effective_user.id,
            "cafes_coords",
            encoding="utf-8",
        )
    )
    keyboard = (
        await keyboards.get_cafe_card_buttons(
            1,
            len(cafes_coords),
            cafes_coords[0].get("latitude"),
            cafes_coords[0].get("longitude"),
        )
    )

    raw = base64.b64decode(
        json.loads(
            await redis.hget(
                update.effective_user.id,
                "cafes_images",
            )
        )[0]
    )

    image = pickle.loads(raw)
    await update.message.reply_photo(
        image,
        json.loads(
            await redis.hget(
                update.effective_user.id,
                "cafes",
                encoding="utf-8",
            )
        )[0],
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard,
    )


async def message_contact(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    async with (
        sessionmanager.session() as session
    ):
        user_profile = await models.Profile.get_by_telegram_id(
            session, update.effective_user.id
        )
        if await user_profile.confirm_phone(
            session,
            int(
                update.message.contact.phone_number
            ),
        ):
            await update.message.reply_text(
                "Вы успешно подтвердили номер телефона!",
                parse_mode=ParseMode.HTML,
            )


async def message_text(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    current_state = (
        await redis.hget(
            update.effective_user.id,
            "current_state",
            encoding="utf-8",
            fallback="",
        )
    ).split(":")
    if current_state[0] == "submitting":
        print("CALLED")
        await handlers.state_submitting(
            update, context, current_state
        )
    elif (
        update.effective_message.text
        == "Предложить кофейню"
    ):

        await redis.hset(
            update.effective_user.id,
            "current_state",
            "submitting:cafe:name",
        )

        await update.message.reply_text(
            "Отправь мне название кофейни, "
            "которой тебе не хватает в нашем сервисе",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Назад",
                            callback_data="reset",
                        )
                    ]
                ]
            ),
        )
    elif (
        update.effective_message.text == "Профиль"
    ):
        await handlers.command_profile(
            update, context
        )
    elif (
        update.effective_message.text
        == "Сообщить об ошибке"
    ):

        await redis.hset(
            update.effective_user.id,
            "current_state",
            "submitting:message",
        )

        await update.message.reply_text(
            "Отправь мне сообщение для администрации и я передам его в целости и сохранности",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Назад",
                            callback_data="reset",
                        )
                    ]
                ]
            ),
        )
    else:
        await handlers.command_start(
            update, context
        )
