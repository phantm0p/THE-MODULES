# BOT/handlers/insta_handler.py

import os
from pyrogram import filters
from ..bot import bot
from ..features.insta import download_instagram_reel
import shutil

# Feature: Download Instagram media
@bot.on_message(filters.command("insta"))
async def insta_command(client, message):
    if len(message.command) < 2:
        await message.reply("Please provide an Instagram media link. Usage: /insta {instagram_media_link}")
        return
    
    media_link = message.command[1]
    user_id = message.from_user.id
    message_id = message.id
    download_path = f"downloads/{user_id}_{message_id}"
    os.makedirs(download_path, exist_ok=True)
    
    downloading_message = await message.reply("Downloading the Instagram Reel, please wait...")
    
    video_path, thumbnail_path = download_instagram_reel(media_link, download_path)
    
    try:
        if video_path:
            if thumbnail_path:
                await client.send_video(video=video_path, thumb=thumbnail_path, chat_id=message.chat.id)
                os.remove(thumbnail_path)
            else:
                await client.send_video(video=video_path, chat_id=message.chat.id)
            os.remove(video_path)
        else:
            await message.reply("Failed to download the Instagram media. Please check the link and try again.")
    except Exception as e:
        await message.reply(f"An error occurred: {e}")
    
    # Delete the downloading message
    await client.delete_messages(chat_id=message.chat.id, message_ids=[downloading_message.id])
    
    shutil.rmtree(download_path)
