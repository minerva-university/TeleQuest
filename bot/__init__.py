import os
import json
import logging
import telegram
from pathlib import Path
from telegram.ext import ApplicationBuilder
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# Start Write-Ahead Logs (For app status and debugging)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Start the telegram bot
bot = telegram.Bot(BOT_TOKEN)

# Initialize Updater and Dispatcher
PORT = int(os.environ.get("PORT", 5000))
app = ApplicationBuilder().token(BOT_TOKEN).build()


# read messages JSON file
BASE_DIR = os.path.join(Path(__file__).parent.parent)
messages = messages = json.load(
    open(os.path.join(BASE_DIR, "bot", "messages.json"), encoding="utf-8")
)
