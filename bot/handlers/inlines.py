from html import escape
from uuid import uuid4

from telegram import (
    InlineQueryResultArticle,
    InputTextMessageContent,
    Update,
)
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from bot import generators
from bot import keyboards
from bot.main import pb
from db import models
from db.main import sessionmanager


async def inline_any(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
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
        await user_profile.increment_inline_search_requests(
            session
        )

    query = update.inline_query.query
    lat = update.inline_query.location.latitude
    lon = update.inline_query.location.longitude

    if not query:
        return

    response = await pb.SearchCafesByQueryPerCity(
        query, lat, lon, 3, 0
    )

    res = []

    for cafe in response.cafes:
        serialized_cafe = (
            await generators.generate_cafe_card(
                cafe
            )
        )
        res.append(
            InlineQueryResultArticle(
                id=str(uuid4()),
                title=f"{cafe.name} в {round(cafe.distance, 2)}км от тебя",
                input_message_content=InputTextMessageContent(
                    serialized_cafe,
                    parse_mode=ParseMode.HTML,

                ),
            ),
        )

    await update.inline_query.answer(res)
