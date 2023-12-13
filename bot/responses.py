from telegram import Update
from telegram.ext import ContextTypes
from db.database import (
    get_multiple_messages_by_id,
    store_message_to_db,
    store_multiple_messages_to_db,
)
from db.vectordb import upload_vectors, query, batch_upload_vectors
from db.db_types import (
    AddMessageResult,
    SerializedMessage,
    PCEmbeddingData,
    NoFromUserError,
)
from ai.embedder import embed, batch_embed_messages
from ai.get_answers import ask
from bot.helpers import find_bot_command, send_help_response
from utils.batch import split_into_batches
from bot.messages import messages as bot_messages
import io
import json

MIN_QUESTION_LENGTH = 5


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
            chat_id=chat_id,
            text=bot_messages["start_user"].format(first_name),
            parse_mode="markdown",
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
            chat_id=chat_id,
            text=bot_messages["help"].format(first_name, ""),
            parse_mode="markdown",
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

    # Determine if the message is new or edited
    msg = update.edited_message if update.edited_message else update.message

    chat_id = effective_chat.id if effective_chat else None

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
                _ = chat_id and await context.bot.send_message(
                    chat_id=chat_id,
                    text=bot_messages["no_tagged_question"],
                )
            else:
                await respond_to_question(
                    msg.reply_to_message.text, chat_id, msg.message_id, context
                )
        elif command.startswith("/start"):
            _ = chat_id and await context.bot.send_message(
                chat_id=chat_id,
                text=bot_messages["start_not_allowed_in_group"],
            )
        else:
            _ = chat_id and await context.bot.send_message(
                chat_id=chat_id,
                text=bot_messages["unrecognized_command"],
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


async def history(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Receive a chat history as a json file and save it.
    """

    # get the user's chat id and first name
    effective_chat = update.effective_chat
    chat_id = effective_chat and effective_chat.id
    if update.message is None:
        return
    if update.message.document is None:
        return
    if chat_id:
        # writing to a custom file
        f = io.BytesIO()
        file = await context.bot.get_file(update.message.document)
        if not file.file_size:
            await context.bot.send_message(
                chat_id=chat_id,
                text=bot_messages["history_empty"],
            )
            return

        # check if the file is bigger than 15MB
        if file.file_size > 1024 * 1024 * 15:
            await context.bot.send_message(
                chat_id=chat_id,
                text=bot_messages["history_too_big"],
            )
            return
        await file.download_to_memory(f)
        f.seek(0)  # start of the file
        try:
            group_chat = json.load(f)
        except json.JSONDecodeError:
            await context.bot.send_message(
                chat_id=chat_id,
                text=bot_messages["history_invalid"],
            )
            return

        try:
            group_chat_id: int = group_chat["id"]
            group_chat_type: str = group_chat["type"]
            group_chat_name: str = group_chat["name"]
            messages = group_chat["messages"]
        except KeyError:
            await context.bot.send_message(
                chat_id=chat_id,
                text=bot_messages["history_invalid"],
            )
            return
        serial_messages: list[SerializedMessage] = []

        for msg in messages:
            try:
                serial_messages.append(
                    SerializedMessage.from_exported_json(
                        msg, group_chat_id, group_chat_type, group_chat_name
                    )
                )
            except NoFromUserError:
                pass
        serial_messages = list(
            filter(lambda msg: msg.text not in [None, ""], serial_messages)
        )
        message_batches_from_embedding = split_into_batches(serial_messages, 2000)
        texts: list[str] = [message.text for message in serial_messages]  # type: ignore
        batch_index = 0
        for embedding_batch in batch_embed_messages(texts):
            embedding_data: list[PCEmbeddingData] = [
                {
                    "id": f"{group_chat_id}:{message.id}",
                    "values": embedding,
                    "metadata": {"chat_id": group_chat_id},
                }
                for message, embedding in zip(
                    message_batches_from_embedding[batch_index], embedding_batch
                )
            ]
            batch_upload_vectors(embedding_data)
            batch_index += 1
        store_multiple_messages_to_db(group_chat_id, serial_messages)
        await context.bot.send_message(
            chat_id=chat_id,
            text=bot_messages["history_upload_success"].format(
                serial_messages[0].chat_title or "the group"
            ),
        )
