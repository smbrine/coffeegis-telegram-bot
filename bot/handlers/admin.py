import asyncio
import base64
import io
import json
import pickle
from datetime import datetime

import grpc
from telegram import (
    Update,
)
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from app.main import redis
from bot import generators, keyboards

from bot.main import img_svc, pb
from db import models
from db.main import sessionmanager


async def admin_command_all_cafes_list(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    user_id = update.effective_user.id
    async with (
        sessionmanager.session() as session
    ):
        user_profile = await models.Profile.get_by_telegram_id(
            session,
            user_id,
            joined=True,
        )

        await redis.hset(
            user_id,
            "profile",
            pickle.dumps(user_profile),
        )
        if not user_profile.is_admin:
            return
    response = await pb.ListCafesPerCity(
        0,
        0,
        100,
        bypass_cache=True,
    )
    list = ""
    for i, cafe in enumerate(response.cafes):
        list += f"{i+1}. {cafe.name}: {cafe.address}.\n"
    await update.message.reply_text(list)


async def admin_command_all_cafes(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    user_id = update.effective_user.id
    async with (
        sessionmanager.session() as session
    ):
        user_profile = await models.Profile.get_by_telegram_id(
            session,
            user_id,
            joined=True,
        )
        await redis.hset(
            user_id,
            "profile",
            pickle.dumps(user_profile),
        )
        if not user_profile.is_admin:
            return

    response = await pb.ListCafesPerCity(
        0,
        0,
        100,
        bypass_cache=True,
    )

    cafes = []

    cafes_coords = []
    cafes_images = []

    # TODO: send placeholder if no cafes in response
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
    print(cafes_coords)
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


async def admin_command_all_cafes_map(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    user_id = update.effective_user.id
    async with (
        sessionmanager.session() as session
    ):
        user_profile = await models.Profile.get_by_telegram_id(
            session,
            user_id,
            joined=True,
        )
        await redis.hset(
            user_id,
            "profile",
            pickle.dumps(user_profile),
        )
        if not user_profile.is_admin:
            return
    response = await pb.ListCafesPerCity(
        0,
        0,
        100,
        bypass_cache=True,
    )
    csv = '"name","lat","lon","address"\n'
    for i, cafe in enumerate(response.cafes):
        csv += f'"{cafe.name}","{cafe.latitude}","{cafe.longitude}","{cafe.address}"\n'
    csv_bytes = io.BytesIO(csv.encode("utf-8"))
    await update.message.reply_document(
        csv_bytes,
        filename=f"map-{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv",
    )


async def admin_command_drop_cache(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    user_id = update.effective_user.id
    async with (
        sessionmanager.session() as session
    ):
        user_profile = await models.Profile.get_by_telegram_id(
            session,
            user_id,
            joined=True,
        )
        if not user_profile.is_admin:
            return
        await redis.hset(
            user_id,
            "profile",
            pickle.dumps(user_profile),
        )

    tasks = []
    tasks.append(redis.drop_cache(user_id))
    tasks.append(
        pb.ListCafesPerCity(
            lat=0, lon=0, drop_cache=True
        )
    )

    await asyncio.gather(*tasks)
