# BOT/database.py

from pymongo import MongoClient
from .config import MONGO_URL

client = MongoClient(MONGO_URL)
db = client["telegram_bot_db"]

# Collection for storing start links and associated user IDs
start_links_collection = db["start_links"]

def store_start_link_data(user_id, start_link_token):
    start_links_collection.insert_one({
        "user_id": user_id,
        "start_link_token": start_link_token
    })

def get_user_by_start_link_token(start_link_token):
    return start_links_collection.find_one({"start_link_token": start_link_token})

def remove_start_link_data(start_link_token):
    start_links_collection.delete_one({"start_link_token": start_link_token})
