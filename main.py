import logging
from utils.logger import setup_logging
from telegram.ext import Application, CommandHandler

from config import BOT_TOKEN, CHECK_INTERVAL
from bot.handlers.register import register_handlers
from bot.commands import set_bot_commands
from database.repositories.topics import seed_topics
from jobs.habr_checker import habr_checker_job


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

async def post_init(application: Application):
    await seed_topics()
    await set_bot_commands(application)

    application.job_queue.run_repeating(
        habr_checker_job,
        interval=CHECK_INTERVAL,
        first=10,
        name="habr_checker",
    )


def main():
    setup_logging()

    application = Application.builder().token(BOT_TOKEN).post_init(post_init).build()

    register_handlers(application)

    application.run_polling()


if __name__ == "__main__":
    main()
