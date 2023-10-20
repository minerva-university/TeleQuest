import pinecone
from typing import List, Dict, Union, Any

# Initialize Pinecone
def initialize_pinecone(api_key: str) -> None:
    pinecone.init(api_key=api_key)

# Create a Pinecone Index
def create_index(index_name: str) -> pinecone.Index:
    pinecone.create_index(name=index_name, metric='cosine', shards=1)
    return pinecone.Index(name=index_name)

# Uploading Vectors
def upload_vectors(index: pinecone.Index, message_embeddings: List[Dict[str, Any]]) -> None:
    index.upsert(items=message_embeddings)

# Querying the Index
def query_index(index: pinecone.Index, query_vector: List[float], top_k: int = 5) -> Dict[str, List[Dict[str, Union[str, float, List[float]]]]]:
    results = index.query(queries=[query_vector], top_k=top_k)
    return results

# Delete the Index (if needed)
def delete_index(index_name: str) -> None:
    pinecone.delete_index(name=index_name)