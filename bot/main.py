import os
from bot.responses import start, help, handle_message, history
from telegram.ext import ApplicationBuilder, Application, filters
from telegram.ext import filters
from telegram.ext import CommandHandler, MessageHandler, ContextTypes


def init(
    deploy: bool = False,
) -> tuple[Application, MessageHandler[ContextTypes.DEFAULT_TYPE], int, str]:  # type: ignore
    BOT_TOKEN = os.getenv("BOT_TOKEN" if deploy else "LOCAL_BOT_TOKEN", "")

    # Initialize Updater and Dispatcher
    PORT = int(os.environ.get("PORT", 5000))
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # add a message handler
    msg_handler = MessageHandler(filters.ChatType.GROUPS & filters.ALL, handle_message)
    return app, msg_handler, PORT, BOT_TOKEN


# main app
def main(
    app: Application,  # type: ignore
    msg_handler: MessageHandler[ContextTypes.DEFAULT_TYPE],
    PORT: int,
    BOT_TOKEN: str,
    deploy: bool = False,
) -> None:
    app.add_handler(CommandHandler("start", start, filters=~filters.ChatType.GROUPS))
    app.add_handler(CommandHandler("help", help, filters=~filters.ChatType.GROUPS))
    app.add_handler(MessageHandler(~filters.ChatType.GROUPS, history))
    # Message handler for new and edited messages in groups
    # Combines filters for messages and edited messages
    combined_filter = filters.ChatType.GROUPS & (
        filters.UpdateType.MESSAGES | filters.UpdateType.EDITED_MESSAGE
    )
    app.add_handler(MessageHandler(combined_filter, handle_message))

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
