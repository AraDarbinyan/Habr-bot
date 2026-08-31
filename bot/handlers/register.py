from telegram.ext import CommandHandler

from bot.handlers.start import start


def register_handlers(application):
    application.add_handler(
        CommandHandler("start", start)
    )
