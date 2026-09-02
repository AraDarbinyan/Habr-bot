import logging

from telegram import Bot
from telegram.error import TelegramError

from bot.constants.topics import TOPICS
from database.models import Topic
from database.repositories.subscriptions import get_topic_subscribers
from parser.schemas import Article


logger = logging.getLogger(__name__)


async def notify_topic_subscribers(
    bot: Bot,
    topic: Topic,
    article: Article,
) -> tuple[int, int]:
    subscribers = await get_topic_subscribers(topic.id)

    display_name = TOPICS.get(
        topic.name,
        topic.name,
    )

    text = (
        f"📰 Новая статья по теме {display_name}\n\n"
        f"{article.title}\n\n"
        f"{article.url}"
    )

    sent = 0
    failed = 0

    for telegram_id in subscribers:
        try:
            await bot.send_message(
                chat_id=telegram_id,
                text=text,
            )
            sent += 1

        except TelegramError:
            failed += 1

            logger.exception(
                "Failed to send article %s to user %s",
                article.id,
                telegram_id,
            )

    return sent, failed
