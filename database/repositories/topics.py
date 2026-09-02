from sqlalchemy import select

from bot.constants.topics import HABR_URLS
from database.database import async_session
from database.models import Topic, Subscription


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

async def get_active_topics() -> list[Topic]:
    async with async_session() as session:
        result = await session.execute(
            select(Topic)
            .join(
                Subscription,
                Subscription.topic_id == Topic.id,
            )
            .distinct()
            .order_by(Topic.name)
        )

        return list(result.scalars().all())
