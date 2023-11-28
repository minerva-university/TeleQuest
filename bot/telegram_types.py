import datetime
from typing import Literal, NotRequired, TypedDict

TMessageKey = Literal[
    "id",
    "type",
    "date",
    "from",
    "from_id",
    "reply_to_message_id",
    "text",
    "text_entities",
]
TTextEntity = TypedDict(
    "TTextEntity",
    {
        "type": str,
        "text": str,
        "user_id": int,
    },
)

TUser = TypedDict(
    "TUser",
    {
        "id": int,
        "is_bot": bool,
        "first_name": str,
        "username": str,
        "last_name": NotRequired[str],
        "language_code": str,
    },
)

TMessage = TypedDict(
    "TMessage",
    {
        "id": int,
        "date": datetime.datetime,
        "from_user": TUser,
        "reply_to_message": int | None,
        "text": str | list[TTextEntity] | None,
        "text_entities": NotRequired[list[TTextEntity]],
        "chat_title": str | None,
    },
)
