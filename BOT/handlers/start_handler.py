# BOT/handlers/start_handler.py

from pyrogram import filters
from ..bot import bot

@bot.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    """
    Handle the /start command. This command is typically used to start interaction with the bot.
    """
    await message.reply_text("Hello! I am your Telegram bot. How can I assist you today?")
