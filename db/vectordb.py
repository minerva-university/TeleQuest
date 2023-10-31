import pinecone
from typing import Sequence, cast
from dotenv import load_dotenv
import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.absolute()))
from db.db_types import PCEmbeddingData, PCQueryResults


load_dotenv()

pinecone.init(
    api_key=os.environ["PINECONE_KEY"], environment=os.environ["PINECONE_ENV"]
)

embedding_index: pinecone.Index = pinecone.Index(pinecone.list_indexes()[0])


def upload_vectors(
    index: pinecone.Index, message_embeddings: Sequence[PCEmbeddingData]
) -> None:
    """
    Uploads a list of message embeddings to the Pinecone index.
    Max recommended length of message_embeddings is 100.
    Parameters
    ----------
    index : pinecone.Index
                The Pinecone index to upload the vectors to.
        message_embeddings : Sequence[PCEmbeddingData]
                The list of message embeddings to upload to the Pinecone index. Each element is of the form
                {"id": <string>, "values": <list[float]>, "metadata": <dict[str, Any]>}.
    """
    return index.upsert(vectors=message_embeddings)  # type: ignore


def query(
    index: pinecone.Index,
    query_vector: list[float],
    top_k: int = 5,
    id: str | None = None,
) -> PCQueryResults:
    """Queries the Pinecone index with a query vector."""
    res = index.query(vector=query_vector, top_k=top_k, id=id)
    results = cast(PCQueryResults, res)
    return results


def delete(index_name: str) -> None:
    """Deletes the Pinecone index."""
    pinecone.delete_index(name=index_name)


if __name__ == "__main__":
    pass