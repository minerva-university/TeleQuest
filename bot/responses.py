import json
from telegram import Update
from telegram.ext import ContextTypes
import sys
from pathlib import Path
import os

BASE_DIR = os.path.join(Path(__file__).parent.parent)
sys.path.append(BASE_DIR)
from db.database import store_message_to_db, read_messages_by_ids
from db.vectordb import upload_vectors, query
from ai.embedder import embed
from ai.get_answers import ask


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

        # TODO: Logic for when to store to the database.
        store_message_success = store_message_to_db(chat_id, msg)
        if not msg.text or not store_message_success:
            return
        if not chat_id:
            return
        embedding_ = embed([msg.text])
        embedding: list[float] = embedding_[0]
        upload_vectors([{"id": f"{chat_id}:{msg.message_id}", "values": embedding}])
        await context.bot.send_message(chat_id=chat_id, text="Success.")

    # if message contains a bot command '/start'
    else:
        # TODO: Handle specific bot commands.
        pass


async def respond_to_question(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    This function is the response of the bot when a user sends a question
    ---
    Parameters:
    update: telegram.Update
        The update object that is received from the telegram bot
    context: telegram.ext.Context
        The context object that is received from the telegram bot.
    """
    effective_chat = update.effective_chat
    message = update.message
    chat_id = effective_chat.id if effective_chat else None
    if not chat_id or not message:
        return
    if not message.text:
        return
    print(message.text)
    # embedding_ = embed([message.text])
    # embedding: list[float] = embedding_[0]
    # top_3 = query(embedding, top_k=3, id=f"{chat_id}:{message.message_id}")["matches"]
    # msg_ids: list[int] = [int(msg["id"]) for msg in top_3]
    # messages = read_messages_by_ids(chat_id, msg_ids)
    # message_texts: list[str] = filter(
    #     lambda t: isinstance(t, str), [msg["text"] for msg in messages]
    # )  # type: ignore
    # message_texts = list(message_texts)
    # resp = ask(message.text, message_texts, print_message=True)
    # if resp:
    #     await context.bot.send_message(chat_id=chat_id, text=resp)
