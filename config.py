import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("HABR_BOT_TOKEN")
DATABASE_URL = os.getenv( "DATABASE_URL")
CHECK_INTERVAL = 10 * 60
