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
    if update.message is None:
        return

    text = (
        "👋 Добро пожаловать в Habr for you!\n\n"
        "Я отслеживаю новые статьи на Habr по интересующим вас "
        "IT-темам и присылаю их прямо сюда.\n\n"
        "Выберите категорию ниже, а затем одну или несколько тем, "
        "на которые хотите подписаться.\n\n"
        "Используйте /help, чтобы посмотреть доступные команды."
    )

    await update.message.reply_text(
        text=text,
        reply_markup=get_topic_groups_keyboard(),
    )

