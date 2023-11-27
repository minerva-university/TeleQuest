import os
import sys
from pathlib import Path

import certifi
import pymongo
from typing import List, Any, Dict
from dotenv import load_dotenv
from pymongo.collection import Collection
from pymongo.command_cursor import CommandCursor

BASE_DIR = os.path.join(Path(__file__).parent.parent)
sys.path.append(BASE_DIR)
from db.db_types import AddMessageResult, GroupChat, SerializedMessage
from bot.telegram_types import TMessage

load_dotenv()

# Connect to the MongoDB Database
client: pymongo.MongoClient[Any] = pymongo.MongoClient(
    os.getenv("MONGO_URI"), tlsCAFile=certifi.where()
)
db = client[os.getenv("DB_NAME", "")]


def store_message_to_db(
    chat_id: int | None, msg: SerializedMessage
) -> AddMessageResult:
    """
    This function stores a given message to the database

    ----
    Parameters:
    chat_id: int | None
        The chat id of the group chat
    msg: telegram.Message | None
        The message object that is to be stored
    """

    # check if the group chat exists, else create a collection for it.
    if not db.active_groups.find_one({"chat_id": chat_id}):
        db.active_groups.insert_one(
            {
                "chat_id": chat_id,
                "group_name": msg.chat_title,
                "categories": [],
            }
        )

    existing_message = db.active_groups.find_one(
        {"chat_id": chat_id, f"messages.{msg.get_id()}": {"$exists": True}}
    )

    if not existing_message:
        add_message_result = db.active_groups.update_one(
            {"chat_id": chat_id},
            {
                "$set": {f"messages.{msg.get_id()}": msg.get_serialized_without_id()},
            },
        )
        if (
            add_message_result.acknowledged
            and add_message_result.matched_count > 0
            and add_message_result.modified_count > 0
        ):
            return AddMessageResult.SUCCESS
        else:
            return AddMessageResult.FAILURE
    else:
        return AddMessageResult.EXISTING


def store_multiple_messages_to_db(
    chat_id: int | None, messages: List[SerializedMessage]
) -> AddMessageResult:
    """
    This function stores a list of messages to the database

    ----
    Parameters:
    chat_id: int | None
        The chat id of the group chat
    messages: List[telegram.Message] | None
        The list of message objects that are to be stored
    """

    # check if the group chat exists, else create a collection for it.
    if not db.active_groups.find_one({"chat_id": chat_id}):
        db.active_groups.insert_one(
            {
                "chat_id": chat_id,
                "group_name": messages[0].chat_title if messages else None,
                "categories": [],
            }
        )

    # Serialize messages without IDs for insertion
    serialized_messages = [msg.get_serialized_without_id() for msg in messages]

    # Insert the messages into the database
    db.active_groups.update_one(
        {"chat_id": chat_id},
        {
            "$push": {"messages": {"$each": serialized_messages}},
        },
    )

    return AddMessageResult.SUCCESS


def read_messages_by_ids(chat_id: int | None, message_ids: list[int]) -> list[TMessage]:
    """
    This function reads a list of messages from the database given their ids.

    ----
    Parameters:
    chat_id: int
        The chat id of the group chat
    message_ids: list[int]
        The list of message ids to be read from the database
    """

    # get the group chat object from the database
    group_chat = db.active_groups.find_one({"chat_id": chat_id})
    if not group_chat:
        return []

    # get the messages from the group chat object
    if "messages" not in group_chat:
        return []
    messages = group_chat["messages"]

    # return the messages that have the message ids in the list of message ids
    return [messages[str(message_id)] for message_id in message_ids]  # type: ignore


def get_multiple_messages_by_id(chat_id: int, message_ids: List[str]) -> List[TMessage]:
    """
    Retrieves a list of messages from the database based on chat_id and message_ids.

    Parameters:
    chat_id: int
        The chat id of the group chat
    message_ids: List[int]
        The list of message IDs to retrieve

    Returns:
    List[SerializedMessage]
        The list of messages that match the given message IDs in the specified chat
    """

    pipeline: List[Dict[str, Any]] = [
        {"$match": {"chat_id": chat_id}},
        {"$project": {"messages": {"$objectToArray": "$messages"}}},
        {"$unwind": "$messages"},
        {"$match": {"messages.k": {"$in": message_ids}}},
        {"$project": {"message": "$messages.v"}},
    ]

    # Execute the aggregation pipeline
    chat_group: CommandCursor[Dict[str, Any]] = db.active_groups.aggregate(pipeline)

    result: list[TMessage] = [msg["message"] for msg in chat_group]

    return result
