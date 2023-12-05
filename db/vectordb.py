import os
import pinecone
from typing import Sequence, cast, Optional
from math import ceil

from .db_types import PCEmbeddingData, PCQueryResults


def init_pinecone() -> Optional[pinecone.Index]:
    if os.getenv("ENVIRONMENT") == "TEST":
        return None  # Bypass in test environment

    pinecone.init(
        api_key=os.environ["PINECONE_KEY"], environment=os.environ["PINECONE_ENV"]
    )
    return pinecone.Index(pinecone.list_indexes()[0])


embedding_index = None
# Use init_pinecone only when necessary and not in a test environment
if os.getenv("ENVIRONMENT") != "TEST":
    embedding_index = init_pinecone()


def batch_upload_vectors(
    index: pinecone.Index | None, all_embeddings: Sequence[PCEmbeddingData]
) -> None:
    """
    Takes in a very large list of embedding data, breaks this into batches of maximum size 100
    and calls the upload_vectors function on each batch.

    Parameters
    ----------
    index : pinecone.Index
            The Pinecone index to upload the vectors to.
    all_embeddings : Sequence[PCEmbeddingData]
            The list of all message embeddings to upload to the Pinecone index.
    """
    if index is None:
        return

    # Define the batch size
    BATCH_SIZE = 100

    # Calculate the number of batches using ceil for more concise and readable code
    num_batches = ceil(len(all_embeddings) / BATCH_SIZE)

    # Loop through each batch and upload
    for i in range(num_batches):
        batch = all_embeddings[i * BATCH_SIZE : (i + 1) * BATCH_SIZE]
        upload_vectors(batch, index)


def upload_vectors(
    message_embeddings: Sequence[PCEmbeddingData],
    index: pinecone.Index | None = embedding_index,
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
    chat_id: int,
    query_vector: list[float],
    top_k: int = 5,
    index: pinecone.Index | None = embedding_index,
) -> PCQueryResults:
    """Queries the Pinecone index with a query vector."""
    if index is None:
        return {"matches": [], "namespace": ""}
    res = index.query(
        vector=query_vector, top_k=top_k, filter={"chat_id": {"$eq": chat_id}}
    )
    results = cast(PCQueryResults, res)
    return results


def delete(index_name: str) -> None:
    """Deletes the Pinecone index."""
    pinecone.delete_index(name=index_name)
