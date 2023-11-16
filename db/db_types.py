from typing import Any, TypedDict, NotRequired, cast
from pymongo.collection import Collection
from enum import Enum
import sys
from pathlib import Path

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


PCEmbeddingMetadata = TypedDict("PCEmbeddingMetadata", {"category": str})
PCEmbeddingData = TypedDict(
    "PCEmbeddingData",
    {"id": str, "values": list[float], "metadata": NotRequired[PCEmbeddingMetadata]},
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
