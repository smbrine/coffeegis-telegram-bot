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
    ChatMemberHandler,
    filters,
)
from app import settings
from utils import ProtoWrapper

bot = Bot(token=settings.TG_BOT_KEY)
dp = ApplicationBuilder().bot(bot).build()
pb = ProtoWrapper(host="localhost:50051")

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    level=logging.INFO,
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
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
