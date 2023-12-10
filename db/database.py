from . import db
from typing import List, Any, Dict
from pymongo.command_cursor import CommandCursor
from db.db_types import AddMessageResult, SerializedMessage
from bot.telegram_types import TMessage


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
                "$set": {f"messages.{msg.get_id()}": msg.get_as_tmessage()},
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

    # Serialize messages with IDs for insertion
    serialized_messages = [msg.get_as_tmessage() for msg in messages]

    # Insert the messages into the database
    db.active_groups.update_one(
        {"chat_id": chat_id},
        {
            "$set": {f"messages.{msg['id']}": msg for msg in serialized_messages},
        },
    )

    return AddMessageResult.SUCCESS


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
