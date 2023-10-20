from typing import Literal, TypedDict

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

TMessage = TypedDict(
    "TMessage",
    {
        "id": str,
        "type": str,
        "date": str,
        "from": str,
        "from_id": str,
        "reply_to_message_id": str,
        "text": str | list[TTextEntity],
        "text_entities": list[TTextEntity],
    },
)
