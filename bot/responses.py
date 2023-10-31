import json
from telegram import Update
from telegram.ext import ContextTypes
import sys
from pathlib import Path
import os

BASE_DIR = os.path.join(Path(__file__).parent.parent)
sys.path.append(BASE_DIR)
from db.database import store_message_to_db


# import messages.json
messages = json.load(
    open(os.path.join(BASE_DIR, "bot", "messages.json"), encoding="utf-8")
)


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
    effective_chat = update.effective_chat
    chat_id = effective_chat and effective_chat.id
    first_name = effective_chat and effective_chat.first_name

    if chat_id:
        # TODO: write a proper message for the user start command
        await context.bot.send_message(
            chat_id=chat_id, text=messages["start_user"].format(first_name)
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
    effective_chat = update.effective_chat

    # get the id of the group chat
    chat_id = effective_chat.id if effective_chat else None

    # get the message object
    msg = update.message

    # if the message is a regular type of message not a bot command
    if msg and not msg.entities:
        # TODO: Logic to handle different types of messages

        _ = chat_id and await context.bot.send_message(
            chat_id=chat_id, text=messages["response"].format("Last message", msg.text)
        )

        # TODO: Logic for when to store to the database.
        store_message = store_message_to_db(chat_id, msg)
    # if message contains a bot command '/start'
    else:
        # TODO: Handle specific bot commands.
        pass
