import os
import json
import logging
import telegram
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder

load_dotenv()


# Start Write-Ahead Logs (For app status and debugging)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# import messages.json
messages = json.load(open("messages.json", encoding="utf-8"))

# Start the telegram bot
bot = telegram.Bot(os.getenv("BOT_TOKEN"))

# Initialize Updater and Dispatcher
PORT = int(os.environ.get('PORT', 5000))
app = ApplicationBuilder().token(os.getenv('BOT_TOKEN')).build()