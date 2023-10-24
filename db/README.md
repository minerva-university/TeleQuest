## Emedding storage

OpenAI's embeddings have 1536 dimensions.

Pinecone's storage uses 4 bytes of storage per dimension.

If we store only 10000 messages per group chat, we would use 59MB per group chat for embeddings alone.

If we store 100,000 messages per group chat, we would use around 590MB per group chat for embeddings alone.