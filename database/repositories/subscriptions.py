from sqlalchemy import select

from database.database import async_session
from database.models import Subscription, Topic, User


async def subscribe_user_to_topic(
    telegram_id: int,
    topic_name: str,
) -> bool:
    async with async_session() as session:
        user_result = await session.execute(
            select(User).where(
                User.telegram_id == telegram_id
            )
        )
        user = user_result.scalar_one_or_none()

        topic_result = await session.execute(
            select(Topic).where(
                Topic.name == topic_name
            )
        )
        topic = topic_result.scalar_one_or_none()

        if user is None:
            raise ValueError("User not found")

        if topic is None:
            raise ValueError("Topic not found")

        subscription_result = await session.execute(
            select(Subscription).where(
                Subscription.user_id == user.id,
                Subscription.topic_id == topic.id,
            )
        )

        subscription = subscription_result.scalar_one_or_none()

        if subscription is not None:
            return False

        subscription = Subscription(
            user_id=user.id,
            topic_id=topic.id,
        )

        session.add(subscription)

        await session.commit()

        return True
