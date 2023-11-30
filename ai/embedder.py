import os
import time
import openai
from openai.error import RateLimitError

from ai.aitypes import EmbedResponseData
from . import EMBEDDING_MODEL
from dotenv import load_dotenv

load_dotenv()

if os.getenv("ENVIRONMENT") != "TEST":
    openai.api_key = os.environ["OPENAI_API_KEY"]


def embed(messages: list[str]) -> list[list[float]]:
    """
    This function embeds the messages using the openai api.
    ---
    Parameters
        messages: list[TMessage]
                The list of messages to be embedded.
    Returns
        embeddings: list[list[float]]
                The list of embeddings of the messages.
    """
    messages = list(filter(lambda msg: msg != "", messages))
    assert 0 < len(messages) < 2001, "The number of messages must be between 1 and 2000"
    embedded = False
    seconds_to_wait: float = 1
    while not embedded:
        try:
            response: EmbedResponseData = openai.Embedding.create(
                model=EMBEDDING_MODEL, input=messages
            )  # type: ignore
            for i, data in enumerate(response["data"]):
                assert (
                    i == data["index"]
                )  # double check embeddings are in same order as input
            embedded = True
        except RateLimitError:
            seconds_to_wait *= 1.2
            print(f"Rate limit error, waiting {seconds_to_wait} seconds...")
            time.sleep(seconds_to_wait)
    return [data["embedding"] for data in response["data"]]  # type: ignore
