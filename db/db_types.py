import json
import sys
from datetime import datetime
from enum import Enum
from pathlib import Path
from pymongo.collection import Collection
from typing import Any, Dict, NotRequired, Optional, Tuple, TypedDict, Union

from telegram import Message, PhotoSize, Video, Voice

sys.path.append(str(Path(__file__).parent.parent.absolute()))
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


class AddMessageResult(Enum):
    SUCCESS = "Success"
    FAILURE = "Failure"
    EXISTING = "Existing"


class SerializedMessage:
    def __init__(self, msg: Message):
        self.id: int = msg.message_id
        self.from_user: Union[Dict[str, Any], None] = (
            json.loads(msg.from_user.to_json()) if msg.from_user else None
        )
        self.date: datetime = msg.date
        self.reply_to_message: Union[int, None] = (
            msg.reply_to_message.message_id if msg.reply_to_message else None
        )
        self.text: Union[str, None] = msg.text
        self.photo: Optional[Tuple[PhotoSize, ...]] = msg.photo
        self.video: Union[Video, None] = msg.video
        self.voice: Union[Voice, None] = msg.voice
        self.chat_title: Union[str, None] = msg.chat.title if msg.chat else None

    def get_serialized_without_id(self) -> Dict[str, Any]:
        return {
            "from_user": self.from_user,
            "date": self.date,
            "reply_to_message": self.reply_to_message,
            "text": self.text,
            "photo": self.photo,
            "video": self.video,
            "voice": self.voice,
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
