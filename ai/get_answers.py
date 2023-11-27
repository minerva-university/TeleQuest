import os
import sys
from pathlib import Path
from dotenv import load_dotenv

from ai.constants import GPT_INFO, INTRODUCTION

BASE_DIR = os.path.join(Path(__file__).parent.parent)
sys.path.append(BASE_DIR)

from typing import Any, cast
from ai.aitypes import (
    ChatCompletion,
)  # for converting embeddings saved as strings back to arrays
import openai  # for calling the OpenAI API
import tiktoken  # for counting tokens

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
    introduction = INTRODUCTION
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
    chat_comp = openai.ChatCompletion.create(  # type: ignore
        model=model,
        messages=messages,
        temperature=temperature,
        **kwargs,
    )
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
    gpt_info = GPT_INFO
    gpt_info[1]["content"] = message
    if print_message:
        print(message)
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
        print("TimeoutError occurred.")  # need to log
        return "I could not find an answer."


if __name__ == "__main__":
    pass
