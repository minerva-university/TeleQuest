from start import *
from telegram import Update
from telegram.ext import ContextTypes
from database import store_message_to_db


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    This function is the response of the bot when a user starts the bot.
    ---
    Parameters:
    update: telegram.Update
        The update object that is received from the telegram bot
    context: telegram.ext.Context
        The context object that is received from the telegram bot.
    """

    # get the user's chat id and first name
    chat_id = update.effective_chat.id
    first_name = update.effective_chat.first_name

    # TODO: write a proper message for the user start command
    await context.bot.send_message(
            chat_id=chat_id,
            text=messages["start_user"].format(first_name)

        )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    This function is the response of the bot when a user sends a message
    to a group.
    ---
    Parameters:
        update: telegram.Update
            The update object that is received from the telegram bot
        context: telegram.ext.Context
            The context object that is received from the telegram bot.
    """
    
    # get the id of the group chat
    chat_id = update.effective_chat.id

    # get the message object
    msg = update.message

    # if the message is a regular type of message not a bot command
    if not msg.entities:
        # TODO: Logic to handle different types of messages

        await context.bot.send_message(
            chat_id=chat_id,
            text=messages["response"].format("Last message", msg.text)
        )

        # TODO: Logic for when to store to the database.
        store_message = store_message_to_db(chat_id, msg)
    # if message contains a bot command '/start'  
    else:
        # TODO: Handle specific bot commands.
        pass