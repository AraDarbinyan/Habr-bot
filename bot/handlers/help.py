from telegram import Update
from telegram.ext import ContextTypes


async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if update.message is None:
        return

    text = (
        "📖 Доступные команды:\n\n"
        "/start — выбрать новые темы для подписки\n"
        "/subscriptions — посмотреть ваши текущие подписки\n"
        "/unsubscribe — отписаться от темы\n"
        "/help — показать это сообщение\n\n"
        "🔔 Бот регулярно проверяет Habr и, если по одной из ваших "
        "тем появляется новая статья, автоматически присылает её вам."
    )

    await update.message.reply_text(text)

