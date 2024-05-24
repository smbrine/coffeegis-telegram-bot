import logging


from telegram import (
    Bot,
    Update,
)
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    InlineQueryHandler,
    MessageHandler,
    filters,
)
from app import settings
from utils import ProtoWrapper, ImagesWrapper

bot = Bot(token=settings.TG_BOT_KEY)
dp = ApplicationBuilder().bot(bot).build()
pb = ProtoWrapper(host="geoprocessor-grpc:50051")
img_svc = ImagesWrapper(host="images-cdn:50051")

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    level=logging.INFO,
)

logging.getLogger("httpx").setLevel(
    logging.DEBUG
    if settings.DEBUG
    else logging.WARNING
)

logger = logging.getLogger(__name__)


def main() -> None:
    from bot import handlers

    dp.add_handler(
        CommandHandler(
            "start", handlers.command_start
        )
    )
    dp.add_handler(
        CommandHandler(
            "all_cafes",
            handlers.admin_command_all_cafes,
        )
    )
    dp.add_handler(
        CommandHandler(
            "all_cafes_list",
            handlers.admin_command_all_cafes_list,
        )
    )
    dp.add_handler(
        CommandHandler(
            "all_cafes_map",
            handlers.admin_command_all_cafes_map,
        )
    )
    dp.add_handler(
        CommandHandler(
            "drop_cache",
            handlers.admin_command_drop_cache,
        )
    )
    dp.add_handler(
        CommandHandler(
            "profile", handlers.command_profile
        )
    )
    dp.add_handler(
        MessageHandler(
            filters.LOCATION,
            handlers.message_location,
        )
    )
    dp.add_handler(
        MessageHandler(
            filters.CONTACT,
            handlers.message_contact,
        )
    )
    dp.add_handler(
        MessageHandler(
            filters.TEXT, handlers.message_text
        )
    )
    dp.add_handler(
        CallbackQueryHandler(
            handlers.callback_any
        )
    )
    dp.add_handler(
        InlineQueryHandler(handlers.inline_any)
    )


main()

if __name__ == "__main__":
    dp.run_polling(
        allowed_updates=Update.ALL_TYPES
    )
