import logging

import aiohttp
from telegram import Bot
from telegram.ext import ContextTypes

from database.repositories.topics import get_active_topics
from services.article_service import process_topic


logger = logging.getLogger(__name__)


async def check_habr_updates(bot: Bot) -> None:
    topics = await get_active_topics()

    if not topics:
        logger.info("No active topics to check")
        return

    timeout = aiohttp.ClientTimeout(total=15)

    async with aiohttp.ClientSession(timeout=timeout) as session:
        for topic in topics:
            try:
                new_article_found = await process_topic(
                    bot=bot,
                    topic=topic,
                    session=session,
                )

                if new_article_found:
                    logger.info(
                        "New article found for topic: %s",
                        topic.name,
                    )

            except Exception:
                logger.exception(
                    "Failed to process topic: %s",
                    topic.name,
                )

async def habr_checker_job(
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    await check_habr_updates(context.bot)
