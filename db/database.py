import os
import json
import certifi
import pymongo
from telegram import Message
from dotenv import load_dotenv
import sys
from pathlib import Path

BASE_DIR = os.path.join(Path(__file__).parent.parent)
sys.path.append(BASE_DIR)
from db.db_types import GroupChat


load_dotenv()

# Connect to the MongoDB Database
client: pymongo.MongoClient[GroupChat] = pymongo.MongoClient(
    os.getenv("MONGO_URI"), tlsCAFile=certifi.where()
)
db = client[os.getenv("DB_NAME", "")]


def store_message_to_db(chat_id: int | None, msg: Message) -> bool:
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
                "group_name": msg.chat.title,
                "categories": [],
            }
        )

    # serialize the telegram message to the format we want
    message = {
        "from_user": msg.from_user
        and json.loads(msg.from_user.to_json()),  # user object
        "date": msg.date,
        # reply_to_message exists if the current message is a reply to a previous one, in which case it references its id.
        "reply_to_message": msg.reply_to_message and msg.reply_to_message.message_id,
        "text": msg.text,
        "photo": msg.photo,
        "video": msg.video,
        "voice": msg.voice,
    }

    existing_message = db.active_groups.find_one(
        {"chat_id": chat_id, f"messages.{msg.message_id}": {"$exists": True}}
    )

    if not existing_message:
        # If the message is not in the database, add it to the messages for that specific group
        add_message_result = db.active_groups.update_one(
            {"chat_id": chat_id},
            {
                "$set": {f"messages.{msg.message_id}": message},
            },
        )
    else:
        # Handle the case where the message already exists, if necessary
        print("Message already exists in the database.")

    # return true if the message was successfully acknowledged by the db, and if the message was successfully modified
    return (
        add_message_result.acknowledged
        and add_message_result.matched_count > 0
        and add_message_result.modified_count > 0
    )
