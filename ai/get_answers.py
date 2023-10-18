from typing import cast
from aitypes import (
    ChatCompletion,
    EmbedResponseData,
)  # for converting embeddings saved as strings back to arrays
import openai  # for calling the OpenAI API
import pandas as pd  # for storing text and embeddings data
import tiktoken  # for counting tokens
from scipy import (
    spatial,
)  # for calculating vector similarities for search
from read_chat_export import read_messages
from read_embed_results import read_embeddings

EMBEDDING_MODEL = "text-embedding-ada-002"  # OpenAI's best embeddings as of Apr 2023
GPT_MODEL = "gpt-3.5-turbo"
openai.api_key_path = "./key"


messages: list[str]
_, messages = read_messages()

messages = messages[-7000:]  # last 7k messages
embeddings = read_embeddings()

df = pd.DataFrame({"text": messages, "embedding": embeddings})


# search function
def strings_ranked_by_relatedness(
    query: str,
    df: pd.DataFrame,
    relatedness_fn=lambda x, y: 1 - spatial.distance.cosine(x, y),
    top_n: int = 100,
) -> tuple[list[str], list[float]]:
    """Returns a list of strings and relatednesses, sorted from
    most related to least."""
    query_embedding_response: EmbedResponseData
    query_embedding_response = openai.Embedding.create(
        model=EMBEDDING_MODEL,
        input=query,
    )  # type: ignore
    query_embedding = query_embedding_response["data"][0]["embedding"]
    strings_and_relatednesses: list[tuple[str, float]] = [
        (row["text"], relatedness_fn(query_embedding, row["embedding"]))
        for i, row in df.iterrows()
    ]  # type: ignore
    strings_and_relatednesses.sort(key=lambda x: x[1], reverse=True)
    strings, relatednesses = zip(*strings_and_relatednesses)
    strings = cast(list[str], strings)  # for type checking
    relatednesses = cast(list[float], relatednesses)
    return strings[:top_n], relatednesses[:top_n]


def num_tokens(text: str, model: str = GPT_MODEL) -> int:
    """Return the number of tokens in a string."""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))


def query_message(query: str, df: pd.DataFrame, model: str, token_budget: int) -> str:
    """Return a message for GPT, with relevant source texts pulled
    from a dataframe."""
    strings, relatednesses = strings_ranked_by_relatedness(query, df)
    introduction = 'The below messages are from individual members of a \
Telegram group chat. Use them to answer the subsequent question. \
If the answer cannot be found in the messages, write "I could not \
find an answer."'
    question = f"\n\nQuestion: {query}"
    message = introduction
    for string in strings:
        next_doc = f'\n\nTelegram Message:\n"""\n{string}\n"""'
        if num_tokens(message + next_doc + question, model=model) > token_budget:
            break
        else:
            message += next_doc
    return message + question


def ask(
    query: str,
    df: pd.DataFrame = df,
    model: str = GPT_MODEL,
    token_budget: int = 4096 - 500,
    print_message: bool = False,
) -> str | None:
    """Answers a query using GPT and a
    dataframe of relevant texts and embeddings."""
    message = query_message(query, df, model=model, token_budget=token_budget)
    if print_message:
        print(message)
    messages = [
        {
            "role": "system",
            "content": "You have access to messages sent from students who \
are members to a Telegram group chat and can answer questions you have seen \
answered previously.",
        },
        {"role": "user", "content": message},
    ]
    response = openai.ChatCompletion.create(
        model=model, messages=messages, temperature=0
    )
    response = cast(ChatCompletion, response)  # for type checking
    response_message = response["choices"][0]["message"]["content"]
    return response_message


if __name__ == "__main__":
    ask("What was the punishment for arriving late to Argentina?")
    # The punishment for arriving late to Argentina was a fine of $100 or more.
