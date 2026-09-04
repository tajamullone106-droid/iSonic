import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    API_ID = int(os.getenv("API_ID", "0"))
    API_HASH = os.getenv("API_HASH", "")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")
    SESSION_STRING = os.getenv("SESSION_STRING", "")
    MONGO_URI = os.getenv("MONGO_URI", "")
    OWNER_ID = int(os.getenv("OWNER_ID", "0"))
    SUPPORT_GROUP = os.getenv("SUPPORT_GROUP", "")
    SUPPORT_CHANNEL = os.getenv("SUPPORT_CHANNEL", "")
    BOT_NAME = os.getenv("BOT_NAME", "Melody")

    # Downloads / cache folder
    DOWNLOADS_DIR = "downloads"

    # Emojis / branding used across messages
    START_IMG = "https://telegra.ph/file/example-thumbnail.jpg"


config = Config()
