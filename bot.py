import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import BOT_TOKEN


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

async def start(update: Update, contex: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💻 Языки программирования", callback_data="example1")],
        [InlineKeyboardButton("🎯 Направления", callback_data="example2")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привет! Я бот который отправляет статьи сайта habr.com по интересуюшим статьям. " \
    "Для начала скажи тебя интересует какой язык или направление в IT тебя интересует", reply_markup=reply_markup)



def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()


if __name__ == '__main__':
    main()
