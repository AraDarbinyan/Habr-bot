from telegram.ext import CommandHandler, CallbackQueryHandler

from bot.handlers.start import start
from bot.handlers.topics import topic_navigation


def register_handlers(application):
    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CallbackQueryHandler(
            topic_navigation,
            pattern=r"^(group:|topics:back)",
        )
    )
