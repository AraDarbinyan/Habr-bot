from telegram import BotCommand


BOT_COMMANDS = [
    BotCommand(
        command="start",
        description="Начать работу с ботом",
    ),
    BotCommand(
        command="subscribe",
        description="Подписаться на новые темы",
    ),
    BotCommand(
        command="subscriptions",
        description="Посмотреть мои подписки",
    ),
    BotCommand(
        command="unsubscribe",
        description="Отписаться от темы",
    ),
    BotCommand(
        command="help",
        description="Помощь и список команд",
    ),
]


async def set_bot_commands(application) -> None:
    await application.bot.set_my_commands(BOT_COMMANDS)
