# BOT/handlers/start_handler.py

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from ..bot import bot
from ..mongo_utils import store_start_link_usage
from ..config import OWNER_ID

@bot.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    """
    Handle the /start command with optional start parameter.
    """
    start_param = message.command[1] if len(message.command) > 1 else None

    if start_param:
        store_start_link_usage(message.from_user.id, start_param)

        await message.reply_text(
            "Welcome! You started the bot with a custom link.",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Link Details", url=f"https://t.me/{client.username}?start={start_param}")]]
            )
        )
    else:
        await message.reply_text("Hello! I am your Telegram bot. How can I assist you today?")

    # Notify the bot owner about the user who started with a custom link
    if start_param:
        await client.send_message(
            OWNER_ID,
            f"User [{message.from_user.first_name}](tg://user?id={message.from_user.id}) started the bot with parameter: {start_param}"
        )

@bot.on_message(filters.command("start_link") & filters.user(OWNER_ID))
async def generate_start_link(client, message):
    """
    Generate a deep linking start URL and send it to the bot owner.
    """
    user_id = message.from_user.id
    unique_start_param = f"get-{user_id}"
    bot_username = (await client.get_me()).username
    start_link = f"https://t.me/{bot_username}?start={unique_start_param}"
    
    await message.reply_text(f"Here is your start link: {start_link}")
