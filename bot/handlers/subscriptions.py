from telegram import Update
from telegram.ext import ContextTypes

from bot.constants.topics import TOPICS
from database.repositories.subscriptions import (
    get_user_subscriptions,
)


async def subscriptions(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    telegram_user = update.effective_user

    if telegram_user is None:
        return

    topic_names = await get_user_subscriptions(
        telegram_id=telegram_user.id
    )

    if not topic_names:
        text = (
            "У вас пока нет подписок.\n\n"
            "Используйте /start, чтобы выбрать интересующие темы."
        )
    else:
        display_names = [
            TOPICS.get(topic_name, topic_name)
            for topic_name in topic_names
        ]

        topics_text = "\n".join(
            f"• {name}"
            for name in display_names
        )

        text = (
            "📚 Ваши подписки:\n\n"
            f"{topics_text}"
        )

    if update.message is not None:
        await update.message.reply_text(text)
