import os
import sys
from pathlib import Path
from telegram import Update
from telegram.ext import ContextTypes

BASE_DIR = os.path.join(Path(__file__).parent.parent)
sys.path.append(BASE_DIR)
from db.database import store_message_to_db
from bot.helpers import find_bot_command, send_help_response, BASE_DIR, messages


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
        await context.bot.send_message(
            chat_id=chat_id, text=messages["start_user"].format(first_name)
        )


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    This function is the response of the bot when a user sends the /help command.
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
        await context.bot.send_message(
            chat_id=chat_id, text=messages["help"].format(first_name, "")
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

    # if the message contains a bot command
    if (
        msg
        and msg.entities
        and any(entity.type == "bot_command" for entity in msg.entities)
    ):
        command = msg.text and find_bot_command(msg.text)

        if command:
            if command.startswith("/help"):
                user_chat_id = msg.from_user.id if msg.from_user else None
                first_name = msg.from_user.first_name if msg.from_user else None
                group_name = msg.chat.title if msg.chat else None
                await send_help_response(
                    context.bot,
                    user_chat_id,
                    first_name,
                    group_name,
                )
            elif command.startswith("/q"):
                parts = msg.text and msg.text.split(maxsplit=1)
                question = parts[1] if parts and len(parts) > 1 else None

                if question or msg.reply_to_message:
                    if not question and msg.reply_to_message:
                        question = msg.reply_to_message.text
                    # TODO: logic to semantically search for the answer to the question, and return an answer.
                    _ = chat_id and await context.bot.send_message(
                        chat_id=chat_id,
                        text=messages["respond_to_question"].format(question),
                    )
            else:
                _ = chat_id and await context.bot.send_message(
                    chat_id=chat_id,
                    text=messages["no_tagged_question"],
                )

    else:
        # TODO: Logic to handle different types of messages

        _ = chat_id and await context.bot.send_message(
            chat_id=chat_id,
            text=messages["response"].format("Last message", msg and msg.text),
        )

        # TODO: Logic for when to store to the database.
        store_message = msg and store_message_to_db(chat_id, msg)
