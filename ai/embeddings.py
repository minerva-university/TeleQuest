import aiohttp
import asyncio
import os
from read_chat_export import read_messages

# Define the OpenAI API endpoint for embeddings
OPENAI_API_ENDPOINT = "https://api.openai.com/v1/embeddings"
API_KEY = os.getenv("OPENAI_API_KEY")  # Assuming the API key is stored as an environment variable

async def call_openai_api(text):
    """
    Call the OpenAI API to generate an embedding for the given text.

    Args:
    text (str): The input text.

    Returns:
    list: The embedding vector.
    """
    headers = {"Authorization": f"Bearer {API_KEY}"}
    payload = {"input": text}
    
    async with aiohttp.ClientSession() as session:
        async with session.post(OPENAI_API_ENDPOINT, headers=headers, json=payload) as response:
            response_data = await response.json()
            if "error" in response_data:
                raise Exception(f"Error from OpenAI API: {response_data['error']}")
            return response_data["data"][0]["embedding"]

def generate_embedding(text):
    """
    Generate an embedding for the given text using the OpenAI API.

    Args:
    text (str): The input text.

    Returns:
    list: The embedding vector.
    """
    return asyncio.run(call_openai_api(text))

def generate_embeddings_for_chat_export():
    """
    Generate embeddings for messages from the chat export.
    """
    _, messages = read_messages()
    embeddings = []

    for message in messages:
        embedding = generate_embedding(message)
        embeddings.append(embedding)

    return embeddings

if __name__ == "__main__":
    embeddings = generate_embeddings_for_chat_export()
    print(f"Generated {len(embeddings)} embeddings.")