import os
from typing import Any, cast
from ai.constants import GPT_INFO, INTRODUCTION
from ai.aitypes import (
    ChatCompletion,
)  # for converting embeddings saved as strings back to arrays
import openai  # for calling the OpenAI API
import tiktoken  # for counting tokens

from utils import timeout, TimeoutError
from . import GPT_MODEL


def num_tokens(text: str, model: str = GPT_MODEL) -> int:
    """
    Return the number of tokens in a string.

    Parameters:
    text (str): The input text.
    model (str): The model to use for tokenization. Defaults to GPT_MODEL.

    Returns:
    int: The number of tokens in the input text.
    """
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))


def query_message(
    query: str,
    messages: list[str],
    model: str = GPT_MODEL,
    token_budget: int = 4096 - 500,
) -> str:
    """
    Return a message for GPT.

    Args:
        query (str): The query to be included in the message.
        messages (list[str]): List of messages to be included in the message.
        model (str, optional): The GPT model to use. Defaults to GPT_MODEL.
        token_budget (int, optional): The maximum token budget for the message. Defaults to 4096 - 500.

    Returns:
        str: The generated message for GPT.
    """
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
    """
    Create a chat completion request.

    Args:
        model (str): The name or ID of the model to use for chat completion.
        messages (list[dict[str, str]]): The list of messages in the conversation.
        temperature (int): Controls the randomness of the output. Higher values make the output more random.
        **kwargs (Any): Additional keyword arguments to pass to the ChatCompletion.create method.

    Returns:
        ChatCompletion: The chat completion response.

    Raises:
        TimeoutError: If the chat completion request times out.
    """
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
    """
    Answers a query using GPT and a
    dataframe of relevant texts and embeddings.

    Args:
        query (str): The query to be answered.
        messages (list[str]): A list of relevant texts and embeddings.
        model (str, optional): The GPT model to use. Defaults to GPT_MODEL.
        token_budget (int, optional): The maximum number of tokens to use for the response. Defaults to 4096 - 500.
        print_message (bool, optional): Whether to print the generated message. Defaults to False.

    Returns:
        str | None: The generated response message, or None if an error occurred.
    """
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
