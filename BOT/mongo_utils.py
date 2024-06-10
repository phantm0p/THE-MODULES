# BOT/mongo_utils.py

from pymongo import MongoClient
from .config import MONGO_URL

# Initialize MongoDB client and select the database
client = MongoClient(MONGO_URL)
db = client['telegram_bot_db']  # Replace with your preferred database name

def get_collection(collection_name):
    return db[collection_name]

def store_start_link_usage(user_id, start_param):
    collection = get_collection('start_links')
    collection.update_one(
        {"user_id": user_id},
        {"$set": {"start_param": start_param}},
        upsert=True
    )

def get_start_link_usage(user_id):
    collection = get_collection('start_links')
    return collection.find_one({"user_id": user_id})
