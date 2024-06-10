# BOT/bot.py

from pyrogram import Client
from .config import bot_token, api_id, api_hash


# Initialize the bot client
bot = Client(
    "my_bot",  # Name of the session
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token,
)


