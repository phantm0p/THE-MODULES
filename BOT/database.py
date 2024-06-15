# BOT/database.py

from pymongo import MongoClient
from .config import MONGO_URL
from datetime import datetime


client = MongoClient(MONGO_URL)
db = client["telegram_bot_db"]
afk_collection = db["afk_status"]
# Collection for storing start links and associated user IDs
start_links_collection = db["start_links"]

# Collection for storing couple data
couples_collection = db["couples"]

def store_start_link_data(user_id, start_link_token):
    start_links_collection.insert_one({
        "user_id": user_id,
        "start_link_token": start_link_token
    })

def get_user_by_start_link_token(start_link_token):
    return start_links_collection.find_one({"start_link_token": start_link_token})

def remove_start_link_data(start_link_token):
    start_links_collection.delete_one({"start_link_token": start_link_token})

async def get_couple(chat_id, date):
    return couples_collection.find_one({"chat_id": chat_id, "date": date})

async def save_couple(chat_id, date, couple):
    couples_collection.update_one(
        {"chat_id": chat_id, "date": date},
        {"$set": {"c1_id": couple["c1_id"], "c2_id": couple["c2_id"]}},
        upsert=True
    )

