import os
import certifi
import pymongo
from dotenv import load_dotenv
from typing import Any

load_dotenv()

# Connect to the MongoDB Database
client: pymongo.MongoClient[Any] = pymongo.MongoClient(
    os.getenv("MONGO_URI"), tlsCAFile=certifi.where()
)

db = client[os.getenv("DB_NAME", "")]
