# BOT/handlers/pin_handler.py

import os
import shutil
from pyrogram import filters
from ..bot import bot
from ..features.pin import download_pinterest_media

# Feature: Download Pinterest media
@bot.on_message(filters.command("pnt") & filters.private)
async def pin_command(client, message):
    if len(message.command) < 2:
        await message.reply("Please provide a Pinterest link. Usage: /pin {pinterest_link}")
        return
    
    pin_url = message.command[1]
    user_id = message.from_user.id
    message_id = message.id
    download_path = f"downloads/{user_id}_{message_id}"
    os.makedirs(download_path, exist_ok=True)
    
    downloading_message = await message.reply("Downloading the Pinterest media, please wait...")

    try:
        # Download the Pinterest media
        media_path = download_pinterest_media(pin_url, download_path)
        
        if media_path:
            # Send the media file to the user
            if media_path.lower().endswith(('mp4', 'mkv', 'webm')):
                await client.send_video(chat_id=message.chat.id, video=media_path)
            else:
                await client.send_photo(chat_id=message.chat.id, photo=media_path)
            
            # Delete the media file from the local storage
            os.remove(media_path)
        else:
            await message.reply("Failed to download the Pinterest media. Please check the link and try again.")
    
    except Exception as e:
        await message.reply(f"An error occurred: {e}")

    # Delete the downloading message
    await client.delete_messages(chat_id=message.chat.id, message_ids=[downloading_message.id])

    # Clean up the download directory
    shutil.rmtree(download_path)
