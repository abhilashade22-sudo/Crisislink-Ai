
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

mongo_client = None
mongo_db = None


def init_mongodb():
    global mongo_client, mongo_db

    mongodb_uri = os.getenv("MONGODB_URI")
    database_name = os.getenv("MONGODB_DB", "crisislink_ai")

    if not mongodb_uri:
        raise ValueError("MONGODB_URI is missing from .env")

    mongo_client = MongoClient(
        mongodb_uri,
        serverSelectionTimeoutMS=10000
    )

    # Verify Atlas connectivity
    mongo_client.admin.command("ping")

    mongo_db = mongo_client[database_name]

    # Create an index for conversation history
    mongo_db.conversations.create_index(
        [("session_id", 1), ("created_at", -1)]
    )

    print("MongoDB connected successfully!")

    return mongo_db


def get_mongodb():
    if mongo_db is None:
        raise RuntimeError("MongoDB has not been initialized.")

    return mongo_db
