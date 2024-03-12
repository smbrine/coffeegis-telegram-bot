import asyncio

from telegram import Update
from telegram.ext import ContextTypes

from bot import generators, keyboards
from db import models
from db.main import sessionmanager


async def command_start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    tasks = []

    msg = (
        "Привет! CoffeeGIS - сервис поиска кофеен. "
        "Отправь мне свою геопозицию и я подскажу где неподалёку есть кофейни из нашей подборки!"
    )

    async with (
        sessionmanager.session() as session
    ):
        if not (
            user_profile := await models.Profile.get_by_telegram_id(
                session, update.effective_user.id
            )
        ):
            await models.Profile.create(
                session,
                user_telegram_id=update.effective_user.id,
            )
            user_profile = await models.Profile.get_by_telegram_id(
                session, update.effective_user.id
            )

        is_phone_confirmed = (
            user_profile.is_phone_confirmed
        )

    keyboard = await keyboards.get_start_keyboard(
        is_phone_confirmed
    )
    context.user_data["current_state"] = "start"

    tasks.append(
        update.message.reply_text(
            msg,
            reply_markup=keyboard,
        )
        if update.message
        else update.callback_query.edit_message_text(
            msg
        )
    )

    await asyncio.gather(*tasks)


async def command_profile(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    async with (
        sessionmanager.session() as session
    ):
        user_profile = await models.Profile.get_by_telegram_id(
            session,
            update.effective_user.id,
            joined=True,
        )
    msg = await generators.generate_profile_card(
        user_profile,
    )
    await update.message.reply_text(msg)
