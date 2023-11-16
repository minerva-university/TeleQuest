import os
import sys
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = os.path.join(Path(__file__).parent.parent)
sys.path.append(BASE_DIR)

from typing import Any, cast
from ai.aitypes import (
    ChatCompletion,
    EmbedResponseData,
)  # for converting embeddings saved as strings back to arrays
import openai  # for calling the OpenAI API
import pandas as pd  # for storing text and embeddings data
import tiktoken  # for counting tokens
from scipy import (  # type: ignore
    spatial,
)  # for calculating vector similarities for search
from ai.read_chat_export import read_messages
from ai.read_embed_results import read_embeddings
from utils import timeout, TimeoutError

load_dotenv()

EMBEDDING_MODEL = "text-embedding-ada-002"  # OpenAI's best embeddings as of Apr 2023
GPT_MODEL = "gpt-3.5-turbo"
openai.api_key = os.environ["OPENAI_API_KEY"]


def num_tokens(text: str, model: str = GPT_MODEL) -> int:
    """Return the number of tokens in a string."""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))


def query_message(
    query: str,
    messages: list[str],
    model: str = GPT_MODEL,
    token_budget: int = 4096 - 500,
) -> str:
    """Return a message for GPT."""
    introduction = 'The below messages are from individual members of a \
Telegram group chat. Use them to answer the subsequent question. Keep the answer fairly short \
and straightforward.\
If the answer cannot be found in the messages, write "I could not \
find an answer."'
    question = f"\n\nQuestion: {query}"
    message = introduction
    for string in messages:
        next_doc = f'\n\nTelegram Message:\n"""\n{string}\n"""'
        if num_tokens(message + next_doc + question, model=model) > token_budget:
            break
        else:
            message += next_doc
    return message + question


@timeout(5)
def create_chat_completion(
    model: str, messages: list[dict[str, str]], temperature: int, **kwargs: Any
) -> ChatCompletion:
    """Create a chat completion request."""
    chat_comp = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        **kwargs,
    )  # type: ignore
    return cast(ChatCompletion, chat_comp)


def ask(
    query: str,
    messages: list[str],
    model: str = GPT_MODEL,
    token_budget: int = 4096 - 500,
    print_message: bool = False,
) -> str | None:
    """Answers a query using GPT and a
    dataframe of relevant texts and embeddings."""
    message = query_message(query, messages, model=model, token_budget=token_budget)
    if print_message:
        print(message)
    gpt_info = [
        {
            "role": "system",
            "content": "You have access to messages sent from people who \
are members of a Telegram group chat and can answer questions you have seen \
answered previously. Your answers are meant to be concise, but contain all relevant information.",
        },
        {"role": "user", "content": message},
    ]
    try:
        resp = openai.ChatCompletion.create(  # type: ignore
            model=model,
            messages=gpt_info,
            temperature=0,
        )
        response = cast(ChatCompletion, resp)  # for type checking
        response_message = response["choices"][0]["message"]["content"]
        return response_message
    except TimeoutError:
        print("TimeoutError occurred.")
        return "I could not find an answer."


if __name__ == "__main__":
    pass
