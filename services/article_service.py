import aiohttp

from telegram import Bot
from services.notification_service import notify_topic_subscribers
from database.models import Topic
from database.repositories.topics import update_last_article_id
from parser.habr_parser import get_latest_article
from parser.schemas import Article


async def check_topic_for_new_article(
    topic: Topic,
    session: aiohttp.ClientSession,
) -> Article | None:

    article = await get_latest_article(
        topic.habr_url,
        session,
    )

    # Тема проверяется впервые.
    # Просто запоминаем текущую статью,
    # но не считаем её новой.
    if topic.last_article_id is None:
        await update_last_article_id(
            topic_id=topic.id,
            article_id=article.id,
        )

        return None

    # Новых статей нет
    if article.id == topic.last_article_id:
        return None

    # Найдена новая статья
    return article

async def process_topic(
    bot: Bot,
    topic: Topic,
    session: aiohttp.ClientSession,
) -> bool:
    article = await check_topic_for_new_article(
        topic=topic,
        session=session,
    )

    if article is None:
        return False

    await notify_topic_subscribers(
        bot=bot,
        topic=topic,
        article=article,
    )

    await update_last_article_id(
        topic_id=topic.id,
        article_id=article.id,
    )

    return True
