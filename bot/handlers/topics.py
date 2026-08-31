from telegram import Update
from telegram.ext import ContextTypes

from bot.keyboards.topics import (
    get_topic_groups_keyboard,
    get_topics_keyboard,
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
