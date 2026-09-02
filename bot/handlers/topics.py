from telegram import Update
from telegram.ext import ContextTypes

from bot.constants.topics import TOPICS
from database.repositories.subscriptions import subscribe_user_to_topic
from bot.keyboards.topics import (
    get_topic_groups_keyboard,
    get_topics_keyboard
)


async def topic_navigation(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query

    if query is None:
        return

    # Убирает "загрузку" на нажатой inline-кнопке
    await query.answer()

    data = query.data

    if data is None:
        return

    if data.startswith("group:"):
        group = data.split(":", maxsplit=1)[1]

        await query.edit_message_text(
            text="Выберите интересующую вас тему:",
            reply_markup=get_topics_keyboard(group),
        )

    elif data == "topics:back":
        await query.edit_message_text(
            text="Выберите категорию:",
            reply_markup=get_topic_groups_keyboard(),
        )


async def subscribe_to_topic(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query

    if query is None:
        return

    # Убираем индикатор загрузки после нажатия кнопки
    await query.answer()

    data = query.data
    telegram_user = update.effective_user

    if data is None or telegram_user is None:
        return

    topic_name = data.split(":", maxsplit=1)[1]

    try:
        created = await subscribe_user_to_topic(
            telegram_id=telegram_user.id,
            topic_name=topic_name,
        )

    except ValueError:
        if query.message is not None:
            await query.message.reply_text(
                "Не удалось найти тему."
            )
        return

    display_name = TOPICS.get(
        topic_name,
        topic_name,
    )

    if query.message is None:
        return

    if created:
        await query.message.reply_text(
            f"✅ Вы подписались на {display_name}"
        )
    else:
        await query.message.reply_text(
            f"ℹ️ Вы уже подписаны на {display_name}"
        )

async def subscribe(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if update.message is None:
        return

    await update.message.reply_text(
        "Выберите категорию интересующих вас тем:",
        reply_markup=get_topic_groups_keyboard(),
    )
