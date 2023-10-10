from telegram_types import TMessage
import json

EMBEDDING_MODEL = (
    "text-embedding-ada-002"  # OpenAI's best embeddings as of Apr 2023
)
BATCH_SIZE = 2000  # you can submit up to 2048 embedding inputs per request


def read_messages(
    fname: str = "M25Chat.json",
) -> tuple[list[TMessage], list[str]]:
    with open(fname, encoding="utf-8") as f:
        data = json.load(f)["messages"]
    data: list[TMessage] = list(filter(lambda d: d["text"] != "", data))
    texts: list[str] = []
    for d in data:
        text = d["text"]
        if isinstance(text, str):
            texts.append(text)
        else:
            s = ""
            for part in text:
                s += part["text"] + " "
            texts.append(s)

    return data, texts


if __name__ == "__main__":
    messages: list[str]
    _, messages = read_messages()

    messages = messages[-7000:]  # last 7k messages

    # write embedding requests to file
    for batch_start in range(0, len(messages), BATCH_SIZE):
        batch_end = batch_start + BATCH_SIZE
        batch = messages[batch_start:batch_end]
        with open(f"embed_m25_chat_reqs_b{BATCH_SIZE}_last7k.jsonl", "a") as f:
            f.write(
                json.dumps(
                    {
                        "model": EMBEDDING_MODEL,
                        "input": batch,
                        "metadata": f"Batch {batch_start} to {batch_end-1}",
                    }
                )
                + "\n"
            )
        print(f"Batch {batch_start} to {batch_end-1}")
