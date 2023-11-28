from typing import Literal

InfoKeys = Literal["role"] | Literal["content"]
GPT_INFO: list[dict[InfoKeys, str]] = [
    {
        "role": "system",
        "content": "You have access to messages sent from people who are members \
of a Telegram group chat and can answer questions you have seen answered previously. \
Your answers are meant to be concise, but contain all relevant information.",
    },
    {"role": "user"},
]

INTRODUCTION = 'The below messages are from individual members of a \
Telegram group chat. Use them to answer the subsequent question. Keep the answer fairly short \
and straightforward.\
If the answer cannot be found in the messages, write "I could not \
find an answer."'
