import time
import openai
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from openai.error import RateLimitError

BASE_DIR = os.path.join(Path(__file__).parent.parent)
sys.path.append(BASE_DIR)
from bot.telegram_types import TMessage
from ai.aitypes import EmbedResponseData

EMBEDDING_MODEL = "text-embedding-ada-002"
load_dotenv()
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


if __name__ == "__main__":
    pass
