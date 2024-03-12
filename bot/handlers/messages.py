from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from bot import handlers, keyboards
from bot.main import pb
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
    context.user_data["cafes"] = []
    context.user_data["cafes_coords"] = []

    for cafe in response.cafes:
        serialized_cafe = (
            await generators.generate_cafe_card(
                cafe
            )
        )
        context.user_data["cafes"].append(
            serialized_cafe
        )
        context.user_data['cafes_coords'].append(
            {
                "latitude": cafe.latitude,
                "longitude": cafe.longitude
            }
        )
    context.user_data["selected_cafe"] = 0
    keyboard = (
        await keyboards.get_cafe_card_buttons(
            1,
            len(context.user_data["cafes"]),
            context.user_data["cafes_coords"][0].get('latitude'),
            context.user_data["cafes_coords"][0].get('longitude')
        )
    )
    await update.message.reply_text(
        context.user_data["cafes"][0],
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
        context.user_data.get("current_state")
        or ""
    ).split(":")
    if current_state[0] == "submitting":
        await handlers.state_submitting(
            update, context, current_state
        )
    elif (
        update.effective_message.text
        == "Предложить кофейню"
    ):
        context.user_data["current_state"] = (
            "submitting:cafe:name"
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
