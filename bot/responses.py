import os
import sys
from pathlib import Path

from telegram import Update
from telegram.ext import ContextTypes

BASE_DIR = os.path.join(Path(__file__).parent.parent)
sys.path.append(BASE_DIR)
from db.database import (
    get_multiple_messages_by_id,
    store_message_to_db,
)
from db.vectordb import upload_vectors, query
from db.db_types import AddMessageResult, SerializedMessage
from ai.embedder import embed
from ai.get_answers import ask
from bot.helpers import find_bot_command, send_help_response, messages

MIN_QUESTION_LENGTH = 10


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

    if not (msg and chat_id):
        return

    if not msg.text:
        return

    # if the message contains a bot command
    if msg.entities and any(entity.type == "bot_command" for entity in msg.entities):
        command = find_bot_command(msg.text)
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
            parts = msg.text.split("/q")
            question = max(parts, key=len).strip()

            if len(question) > MIN_QUESTION_LENGTH:
                await respond_to_question(question, chat_id, msg.message_id, context)
            elif msg.reply_to_message is None or msg.reply_to_message.text is None:
                return
            else:
                await respond_to_question(
                    msg.reply_to_message.text, chat_id, msg.message_id, context
                )
        else:
            _ = chat_id and await context.bot.send_message(
                chat_id=chat_id,
                text=messages["no_tagged_question"],
            )

    else:
        # TODO: Logic to handle different types of messages
        message: SerializedMessage | None = SerializedMessage(msg) if msg else None
        store_message = message and store_message_to_db(chat_id, message)
        store_message_success = store_message == AddMessageResult.SUCCESS
        if not store_message_success:
            return
        if not chat_id:
            return
        embedding_ = embed([msg.text])
        embedding: list[float] = embedding_[0]
        upload_vectors(
            [
                {
                    "id": f"{chat_id}:{msg.message_id}",
                    "values": embedding,
                    "metadata": {"chat_id": chat_id},
                }
            ]
        )


async def respond_to_question(
    question: str, chat_id: int, message_id: int, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    This function is the response of the bot when a user sends a question
    ---
    Parameters:
    question: str
        The question to respond to.
    """
    print(question)
    embedding_ = embed([question])
    embedding: list[float] = embedding_[0]
    top_3 = query(chat_id, embedding, top_k=3)["matches"]
    msg_ids = [msg["id"] for msg in top_3]
    msg_ids = [m_id.split(":")[1] for m_id in msg_ids]
    messages = get_multiple_messages_by_id(chat_id, msg_ids)
    message_texts: list[str] = filter(
        lambda t: isinstance(t, str), [msg["text"] for msg in messages]
    )  # type: ignore
    message_texts = list(message_texts)
    resp = ask(question, message_texts, print_message=True)
    if resp:
        await context.bot.send_message(
            chat_id=chat_id, text=resp, reply_to_message_id=message_id
        )
