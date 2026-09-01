from telegram import Update
from telegram.ext import ContextTypes

from bot.keyboards.topics import get_unsubscribe_keyboard
from bot.constants.topics import TOPICS
from database.repositories.subscriptions import (
    get_user_subscriptions,
    unsubscribe_user_from_topic,
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

async def unsubscribe(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    telegram_user = update.effective_user

    if telegram_user is None or update.message is None:
        return

    topic_names = await get_user_subscriptions(
        telegram_id=telegram_user.id
    )

    if not topic_names:
        await update.message.reply_text(
            "У вас пока нет подписок."
        )
        return

    await update.message.reply_text(
        "Выберите тему, от которой хотите отписаться:",
        reply_markup=get_unsubscribe_keyboard(topic_names),
    )

async def unsubscribe_from_topic(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query

    if query is None:
        return

    await query.answer()

    telegram_user = update.effective_user
    data = query.data

    if telegram_user is None or data is None:
        return

    topic_name = data.split(":", maxsplit=1)[1]

    deleted = await unsubscribe_user_from_topic(
        telegram_id=telegram_user.id,
        topic_name=topic_name,
    )

    display_name = TOPICS.get(
        topic_name,
        topic_name,
    )

    if query.message is None:
        return

    if deleted:
        await query.message.reply_text(
            f"✅ Вы отписались от {display_name}"
        )
    else:
        await query.message.reply_text(
            f"ℹ️ Вы уже не подписаны на {display_name}"
        )
