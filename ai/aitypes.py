from typing import Any, Literal, TypedDict

RequestData = TypedDict(
    "RequestData",
    {
        "model": str,
        "input": list[str],
    },
)

EmbeddingData = TypedDict(
    "EmbeddingData", {"object": str, "index": int, "embedding": list[float]}
)

EmbedResponseData = TypedDict(
    "ResponseData",
    {
        "object": str,
        "data": list[EmbeddingData],
        "model": str,
        "usage": str,
    },
)

OpenAIJSONL = tuple[
    RequestData, EmbedResponseData, dict[Literal["metadata"], Any]
]

CompletionMessage = TypedDict(
    "Message",
    {
        "content": str | None,
        "role": str,
        "function_call": dict[Literal["name", "arguments"], str],
    },
)

CompletionChoice = TypedDict(
    "Choice",
    {
        "message": CompletionMessage,
        "index": int,
        "finish_reason": str,
    },
)

ChatCompletion = TypedDict(
    "ChatCompletion",
    {
        "id": str,
        "object": Literal["chat.completion"],
        "created": int,
        "model": str,
        "choices": list[CompletionChoice],
        "usage": dict[
            Literal["completion_tokens", "prompt_tokens", "total_tokens"], int
        ],
    },
)
