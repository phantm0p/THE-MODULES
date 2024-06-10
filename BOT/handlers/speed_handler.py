# BOT/handlers/spt_handler.py

from pyrogram import Client, filters
from BOT.features import speed  # Import the speed test logic
from BOT.bot import bot  # Import your bot instance

@bot.on_message(filters.command("spt") & filters.private)
async def speedtest_handler(client, message):
    """
    Command handler for /spt to perform a speed test.

    Args:
        client (Client): The Pyrogram client instance.
        message (Message): The message object triggering the command.

    Returns:
        None
    """
    await message.reply_text("Running Speedtest... Please wait.")
    await speed.handle_speedtest(client, message)
