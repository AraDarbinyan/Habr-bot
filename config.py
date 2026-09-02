import os
from dotenv import load_dotenv

load_dotenv()

def get_required_env(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise RuntimeError(
            f"Required environment variable '{name}' is not set"
        )

    return value

BOT_TOKEN = get_required_env("HABR_BOT_TOKEN")
DATABASE_URL = get_required_env("DATABASE_URL")

CHECK_INTERVAL = 10 * 60
