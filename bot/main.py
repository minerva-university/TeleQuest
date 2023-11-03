import os
import sys
from pathlib import Path

BASE_DIR = os.path.join(Path(__file__).parent.parent)
sys.path.append(BASE_DIR)
import logging
import telegram
from bot.responses import respond_to_question, start, handle_message
from telegram.ext import ApplicationBuilder
from telegram.ext import filters
from telegram.ext import CommandHandler, MessageHandler

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

# add a message handler
msg_handler = MessageHandler(filters.ChatType.GROUPS & filters.ALL, handle_message)


# main app
def main(deploy: bool = False) -> None:
    app.add_handler(
        CommandHandler("start", start, filters=~filters.ChatType.GROUPS)
    )  # add specific handler for '/start
    app.add_handler(msg_handler)  # add message handler
    app.add_handler(
        CommandHandler("question", respond_to_question, filters=filters.ChatType.GROUPS)
    )  # add specific handler for '/q

    if deploy:
        # listens for requests from any addresses
        app.run_webhook(
            listen="0.0.0.0",
            port=int(PORT),
            url_path=BOT_TOKEN,
            webhook_url=f"https://tele-quest-ecdd62e1d0d3.herokuapp.com/{os.getenv('BOT_TOKEN')}",
        )

    else:
        app.run_polling()  # this is used to run the bot locally

    app.idle()  # type: ignore


if __name__ == "__main__":
    deploy = "--deploy" in sys.argv or "-d" in sys.argv
    main(deploy=deploy)
