import os
from bot.responses import start, help, handle_message
from telegram.ext import filters
from telegram.ext import CommandHandler, MessageHandler
from . import app, PORT, BOT_TOKEN


# add a message handler
msg_handler = MessageHandler(filters.ChatType.GROUPS & filters.ALL, handle_message)


# main app
def main(deploy: bool = False) -> None:
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
