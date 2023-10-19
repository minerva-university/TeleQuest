from typing import TypedDict, Literal

GroupChat = TypedDict(
    "GroupChat",
    {
        "chat_id": int | None,
        "group_name": str | None,
        "categories": list[str],
    },
)
