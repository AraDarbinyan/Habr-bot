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

CHECK_INTERVAL = 10 * 60
