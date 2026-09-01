from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.topics import LANGUAGES, DIRECTIONS, TOPICS


TOPIC_GROUPS = {
    "languages": LANGUAGES,
    "directions": DIRECTIONS,
}


def get_topic_groups_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                "💻 Языки",
                callback_data="group:languages",
            ),
            InlineKeyboardButton(
                "🧭 Направления",
                callback_data="group:directions",
            ),
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


def get_topics_keyboard(group: str) -> InlineKeyboardMarkup:
    topics = TOPIC_GROUPS.get(group)

    if topics is None:
        raise ValueError(f"Unknown topic group: {group}")

    buttons = [
        InlineKeyboardButton(
            text=display_name,
            callback_data=f"topic:{topic_name}",
        )
        for topic_name, display_name in topics.items()
    ]

    keyboard = [
        buttons[i:i + 3]
        for i in range(0, len(buttons), 3)
    ]

    keyboard.append(
        [
            InlineKeyboardButton(
                "⬅️ Назад",
                callback_data="topics:back",
            )
        ]
    )

    return InlineKeyboardMarkup(keyboard)

def get_unsubscribe_keyboard(
    topic_names: list[str],
) -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(
            text=TOPICS.get(topic_name, topic_name),
            callback_data=f"unsubscribe:{topic_name}",
        )
        for topic_name in topic_names
    ]

    keyboard = [
        buttons[i:i + 2]
        for i in range(0, len(buttons), 2)
    ]

    return InlineKeyboardMarkup(keyboard)
