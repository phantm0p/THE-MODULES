# BOT/handlers/telegraph_handler.py

import os
from pyrogram import filters
from ..bot import bot
from ..features.telegrapph import telegraph_client

# Command Handler: Upload Image to Telegraph
@bot.on_message(filters.reply & filters.command("up"))
async def upload_image(client, message):
    if not message.reply_to_message or not message.reply_to_message.photo:
        await message.reply("Please reply to an image with /up to upload it to Telegraph.")
        return

    # Download the image to the local device
    file_id = message.reply_to_message.photo.file_id
    file = await client.download_media(file_id)
    
    # Upload the image to Telegraph
    telegraph_url = telegraph_client.upload_image(file)

    # Delete the local image file
    os.remove(file)

    # Reply with the Telegraph URL
    await message.reply(f"Image uploaded to Telegraph: {telegraph_url}")
