import pinecone

# Initialize Pinecone
def initialize_pinecone(api_key):
    pinecone.init(api_key=api_key)

# Create a Pinecone Index
def create_index(index_name):
    pinecone.create_index(name=index_name, metric='cosine', shards=1)
    return pinecone.Index(name=index_name)

# Uploading Vectors
def upload_vectors(index, message_embeddings):
    index.upsert(items=message_embeddings)

# Querying the Index
def query_index(index, query_vector, top_k=5):
    results = index.query(queries=[query_vector], top_k=top_k)
    return results[0]

# Delete the Index (if needed)
def delete_index(index_name):
    pinecone.delete_index(name=index_name)