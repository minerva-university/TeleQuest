import json
from aitypes import OpenAIJSONL

EMBEDDING_MODEL = (
    "text-embedding-ada-002"  # OpenAI's best embeddings as of Apr 2023
)
BATCH_SIZE = 2000  # you can submit up to 2048 embedding inputs per request


def read_embeddings() -> list[list[float]]:
    embeddings: list[list[float]] = []
    with open(f"embed_m25_chat_results_b{BATCH_SIZE}_last7k.jsonl") as f:
        for line in f:
            response_line: OpenAIJSONL = json.loads(line)
            response = response_line[1]
            for i, be in enumerate(response["data"]):
                assert (
                    i == be["index"]
                )  # double check embeddings are in same order as input
            batch_embeddings = [e["embedding"] for e in response["data"]]
            embeddings.extend(batch_embeddings)
    return embeddings


if __name__ == "__main__":
    pass
