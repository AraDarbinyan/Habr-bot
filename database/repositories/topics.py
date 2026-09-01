from sqlalchemy import select

from bot.constants.topics import HABR_URLS
from database.database import async_session
from database.models import Topic


async def seed_topics() -> None:
    async with async_session() as session:
        result = await session.execute(
            select(Topic.name)
        )

        existing_topics = set(result.scalars().all())

        new_topics = [
            Topic(
                name=name,
                habr_url=url,
            )
            for name, url in HABR_URLS.items()
            if name not in existing_topics
        ]

        if new_topics:
            session.add_all(new_topics)
            await session.commit()
