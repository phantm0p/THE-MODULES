# BOT/handlers/upload_handler.py

from pyrogram import filters
from ..bot import bot
from ..config import OWNER_ID, LOGGING_CHAT_ID
from ..mongo_utils import get_start_link_usage

@bot.on_message(filters.reply & filters.user(OWNER_ID))
async def handle_upload_command(client, message):
    """
    Handle the /upload command to forward the replied-to message to the logging chat.
    """
    if message.reply_to_message and message.text == "/upload":
        original_message = message.reply_to_message
        await original_message.forward(LOGGING_CHAT_ID)
        await message.reply_text("The message has been forwarded to the logging chat.")

@bot.on_message(filters.private & filters.incoming)
async def forward_to_user(client, message):
    """
    Forward any incoming messages to the user who used a specific start link.
    """
    start_data = get_start_link_usage(message.from_user.id)
    if start_data:
        target_user_id = int(start_data['start_param'].split('-')[1])
        await message.forward(target_user_id)
        await message.reply_text("Your message has been forwarded.")
