# bot/handlers/start.py

from telegram import Update
from telegram.ext import ContextTypes
from database.repositories.users import get_or_create_user
from bot.keyboards.topics import get_topic_groups_keyboard


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

    if update.message is not None:
        await update.message.reply_text(
            "Выберите категорию интересующих вас тем:",
            reply_markup=get_topic_groups_keyboard(),
        )
