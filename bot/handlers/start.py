# bot/handlers/start.py

from telegram import Update
from telegram.ext import ContextTypes
from database.repositories.users import get_or_create_user


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    telegram_user = update.effective_user

    if telegram_user is not None:
        await get_or_create_user(
            telegram_id=telegram_user.id,
            username=telegram_user.username,
        )

    await update.message.reply_text("Привет!")
