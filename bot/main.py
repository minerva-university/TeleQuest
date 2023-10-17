from responses import *
from telegram.ext import filters
from telegram.ext import CommandHandler, MessageHandler

msg_handler = MessageHandler(filters.ChatType.GROUPS & filters.ALL, handle_message)

def main(deploy=False):

    app.add_handler(CommandHandler("start", start, filters=~filters.ChatType.GROUPS)) #add specific handler for '/start
    app.add_handler(msg_handler) # add message handler

    if deploy:
        # listens for requests from any addresses
        app.run_webhook(
            listen='0.0.0.0', 
            port=int(PORT), 
            url_path=os.getenv("BOT_TOKEN"),
            webhook_url=f"https://tele-quest-ecdd62e1d0d3.herokuapp.com/{os.getenv('BOT_TOKEN')}"
        )

    else:
        app.run_polling() # this is used to run the bot locally
    
    app.idle()


if __name__ == "__main__":
    main(deploy=True)