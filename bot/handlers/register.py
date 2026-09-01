from telegram.ext import CommandHandler, CallbackQueryHandler

from bot.handlers.start import start
from bot.handlers.topics import (
    subscribe_to_topic,
    topic_navigation,
)
from bot.handlers.subscriptions import subscriptions


def register_handlers(application):
    application.add_handler(
        CommandHandler("start", start)
    )
    application.add_handler(
        CommandHandler("subscriptions",subscriptions,)
    )

    application.add_handler(
        CallbackQueryHandler(
            topic_navigation,
            pattern=r"^(group:|topics:back)",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            topic_navigation,
            pattern=r"^(group:|topics:back)",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            subscribe_to_topic,
            pattern=r"^topic:",
        )
    )
