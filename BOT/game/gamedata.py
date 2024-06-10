# BOT/game/gamedata.py
from pymongo import MongoClient
from ..config import MONGO_URL
from datetime import datetime

# Establish a connection to the MongoDB database
client = MongoClient(MONGO_URL)
db = client['game_db']
users_collection = db['users']
gifts_collection = db['gifts']

def get_user(user_id):
    return users_collection.find_one({"user_id": user_id})

def create_user(user_id, balance):
    user = {"user_id": user_id, "balance": balance}
    users_collection.insert_one(user)

def update_balance(user_id, new_balance):
    users_collection.update_one({"user_id": user_id}, {"$set": {"balance": new_balance}})

def save_gift_timestamps(sender_id, timestamp):
    gift = {"sender_id": sender_id, "timestamp": timestamp}
    gifts_collection.insert_one(gift)

def get_gift_timestamps(sender_id):
    timestamps = []
    for gift in gifts_collection.find({"sender_id": sender_id}):
        timestamps.append(gift["timestamp"])
    return timestamps

def get_top_users():
    return users_collection.find().sort("balance", -1).limit(10)
