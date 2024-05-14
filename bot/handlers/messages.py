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

    response = await pb.ListCafesPerCity(
        update.message.location.latitude,
        update.message.location.longitude,
        10,
    )

    cafes = []
    # images = [
    #     open(
    #         "./deploy_data/test_images/" + name,
    #         "rb",
    #     ).read()
    #     for name in ["1.png", "2.png", "3.webp"]
    # ]

    cafes_coords = []
    cafes_images = []
    _i = 0
    for cafe in response.cafes:
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
        print(cafe)
        try:
            image_bytes = (
                await img_svc.GetImage(
                    cafe.description.image_uuid
                )
            ).content
            print("Found image")

        except grpc.aio._call.AioRpcError as e:
            print("Defaulting image")
            print(e)
            image_bytes = open(
                "./data/default.webp",
                "rb",
            ).read()

        image = base64.b64encode(
            pickle.dumps(image_bytes)
        ).decode("utf-8")

        cafes_images.append(image)
        # if _i < 3:
        #     cafes_images.append(
        #         base64.b64encode(
        #             pickle.dumps(images[_i])
        #         ).decode("utf-8")
        #     )
        # else:
        #     cafes_images.append(
        #         base64.b64encode(
        #             pickle.dumps(images[2])
        #         ).decode("utf-8")
        #     )
        # _i += 1

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

    keyboard = (
        await keyboards.get_cafe_card_buttons(
            1,
            len(
                json.loads(
                    await redis.hget(
                        update.effective_user.id,
                        "cafes_coords",
                        encoding="utf-8",
                    )
                )
            ),
            json.loads(
                await redis.hget(
                    update.effective_user.id,
                    "cafes_coords",
                    encoding="utf-8",
                )
            )[0].get("latitude"),
            json.loads(
                await redis.hget(
                    update.effective_user.id,
                    "cafes_coords",
                    encoding="utf-8",
                )
            )[0].get("longitude"),
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
