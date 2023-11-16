import os
import sys
from pathlib import Path

import certifi
import pymongo
from typing import List
from dotenv import load_dotenv

BASE_DIR = os.path.join(Path(__file__).parent.parent)
sys.path.append(BASE_DIR)
from db.db_types import AddMessageResult, GroupChat, SerializedMessage

load_dotenv()

# Connect to the MongoDB Database
client: pymongo.MongoClient[GroupChat] = pymongo.MongoClient(
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
