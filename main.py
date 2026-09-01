import logging
from telegram.ext import Application, CommandHandler

from config import BOT_TOKEN
from bot.handlers.register import register_handlers
from database.database import init_db
from database.repositories.topics import seed_topics


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

async def post_init(application: Application):
    await init_db()
    await seed_topics()



def main():
    application = Application.builder().token(BOT_TOKEN).post_init(post_init).build()

    register_handlers(application)

    application.run_polling()


if __name__ == "__main__":
    main()
