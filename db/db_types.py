from typing import TypedDict, NotRequired
from pymongo.collection import Collection
from bot.telegram_types import TMessage

GroupChat = TypedDict(
    "GroupChat",
    {
        "chat_id": int | None,
        "group_name": str | None,
        "categories": list[str],
        "messages": NotRequired[Collection[TMessage]],
    },
)
