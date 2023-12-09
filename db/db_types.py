import json
from datetime import datetime
from enum import Enum
from pymongo.collection import Collection
from typing import NotRequired, Optional, Tuple, TypedDict, Union, Any
from telegram import Message, PhotoSize, Video, Voice, User, Chat

from bot.telegram_types import TMessage, TUser

GroupChat = TypedDict(
    "GroupChat",
    {
        "chat_id": int | None,
        "group_name": str | None,
        "categories": list[str],
        "messages": NotRequired[Collection[TMessage]],
    },
)


class NoFromUserError(Exception):
    def __init__(
        self, message: str = "Message must have a from_user attribute"
    ) -> None:
        super().__init__(message)


class AddMessageResult(Enum):
    SUCCESS = "Success"
    FAILURE = "Failure"
    EXISTING = "Existing"


class SerializedMessage:
    @classmethod
    def from_exported_json(
        cls, json_dict: dict[str, Any], chat_id: int, chat_title: str
    ) -> "SerializedMessage":
        id = json_dict["id"]
        if "from" not in json_dict:
            raise NoFromUserError
        first_name, *other_names = json_dict["from"].split(" ")
        if len(other_names) > 0:
            last_name = other_names[-1]
        else:
            last_name = None
        from_user = {
            "id": json_dict["from_id"],
            "is_bot": False,
            "first_name": first_name,
            "language_code": "en",
        }
        user = User(**from_user)
        if last_name:
            from_user["last_name"] = last_name

        return cls(
            Message(
                id,
                datetime.fromisoformat(json_dict["date"]),
                chat=Chat(chat_id, chat_title),
                from_user=user,
            )
        )

    def __init__(self, msg: Message):
        self.id: int = msg.message_id
        if not msg.from_user:
            raise NoFromUserError
        self.from_user: TUser = json.loads(msg.from_user.to_json())
        self.date: datetime = msg.date
        self.reply_to_message: Union[int, None] = (
            msg.reply_to_message.message_id if msg.reply_to_message else None
        )
        self.text: Union[str, None] = msg.text
        self.photo: Optional[Tuple[PhotoSize, ...]] = msg.photo
        self.video: Union[Video, None] = msg.video
        self.voice: Union[Voice, None] = msg.voice
        self.chat_title: Union[str, None] = msg.chat.title if msg.chat else None

    def get_as_tmessage(self) -> TMessage:
        return {
            "id": self.id,
            "from_user": self.from_user,
            "date": self.date,
            "reply_to_message": self.reply_to_message,
            "text": self.text,
            "chat_title": self.chat_title,
        }

    def get_id(self) -> int:
        return self.id

    def __repr__(self) -> str:
        """Provide a detailed representation for debugging."""
        return (
            f"SerializedMessage(id={self.id}, from_user={self.from_user}, "
            f"date={self.date}, reply_to_message={self.reply_to_message}, "
            f"text={self.text}, photo={self.photo}, video={self.video}, "
            f"voice={self.voice}, chat_title={self.chat_title})"
        )

    def __str__(self) -> str:
        """Provide a user-friendly string representation of the message."""
        return (
            f"Message ID: {self.id}, From: {self.from_user}, Date: {self.date}, "
            f"Reply To: {self.reply_to_message}, Text: {self.text}, "
            f"Photo: {self.photo}, Video: {self.video}, Voice: {self.voice}, "
            f"Chat Title: {self.chat_title}"
        )


PCEmbeddingMetadata = TypedDict(
    "PCEmbeddingMetadata", {"category": NotRequired[str], "chat_id": int}
)
PCEmbeddingData = TypedDict(
    "PCEmbeddingData",
    {"id": str, "values": list[float], "metadata": PCEmbeddingMetadata},
)

PCQueryResult = TypedDict(
    "PCQueryResult",
    {
        "id": str,
        "score": float,
        "values": list[float],
        "metadata": NotRequired[PCEmbeddingMetadata],
    },
)

PCQueryResults = TypedDict(
    "PCQueryResults",
    {"matches": list[PCQueryResult], "total": NotRequired[int], "namespace": str},
)
