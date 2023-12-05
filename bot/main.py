import os
import telegram
from bot.responses import start, help, handle_message
from telegram.ext import ApplicationBuilder, Application
from telegram.ext import filters
from telegram.ext import CommandHandler, MessageHandler


<<<<<<< HEAD
def init(deploy: bool = False) -> tuple[Application, MessageHandler, int, str]:  # type: ignore
    BOT_TOKEN = os.getenv("BOT_TOKEN" if deploy else "LOCAL_BOT_TOKEN", "")

    # Start the telegram bot
    bot = telegram.Bot(BOT_TOKEN)
=======
# def init(deploy: bool = False) -> tuple[Application, MessageHandler, int, str]:
# BOT_TOKEN = os.getenv("BOT_TOKEN" if deploy else "LOCAL_BOT_TOKEN", "")
BOT_TOKEN = os.getenv("LOCAL_BOT_TOKEN", "")

# Start Write-Ahead Logs (For app status and debugging)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Start the telegram bot
bot = telegram.Bot(BOT_TOKEN)
>>>>>>> a7411fd (testing out adding option to run a local bot; bot is not getting messages)

# Initialize Updater and Dispatcher
PORT = int(os.environ.get("PORT", 5000))
app = ApplicationBuilder().token(BOT_TOKEN).build()

# add a message handler
msg_handler = MessageHandler(filters.ChatType.GROUPS & filters.ALL, handle_message)
# return app, msg_handler, PORT, BOT_TOKEN


# main app
def main(
    app: Application,  # type: ignore
    msg_handler: MessageHandler,  # type: ignore
    PORT: int,
    BOT_TOKEN: str,
    deploy: bool = False,
) -> None:
    app.add_handler(CommandHandler("start", start, filters=~filters.ChatType.GROUPS))
    app.add_handler(CommandHandler("help", help, filters=~filters.ChatType.GROUPS))
    app.add_handler(msg_handler)  # add message handler

    if not deploy:
        app.run_polling()  # this is used to run the bot locally
    else:
        # listens for requests from any addresses
        app.run_webhook(
            listen="0.0.0.0",
            port=int(PORT),
            url_path=BOT_TOKEN,
            webhook_url=f"https://tele-quest-ecdd62e1d0d3.herokuapp.com/{os.getenv('BOT_TOKEN')}",
        )

    app.idle()  # type: ignore
<<<<<<< HEAD
=======


if __name__ == "__main__":
    deploy = "--deploy" in sys.argv or "-d" in sys.argv
    # app, msg_handler, PORT, BOT_TOKEN = init(deploy=deploy)
    main(app, msg_handler, PORT, BOT_TOKEN, deploy=deploy)
>>>>>>> a7411fd (testing out adding option to run a local bot; bot is not getting messages)
