# BOT/handlers/yt_handler.py

import os
from pyrogram import filters
from ..bot import bot
from ..features.yt import download_youtube_video
import shutil

# Feature: Download YouTube video
@bot.on_message(filters.command("yt") & filters.private)
async def yt_command(client, message):
    if len(message.command) < 2:
        await message.reply("Please provide a YouTube link. Usage: /yt {youtube_link}")
        return
    
    yt_url = message.command[1]
    user_id = message.from_user.id
    message_id = message.id
    download_path = f"downloads/{user_id}_{message_id}"
    os.makedirs(download_path, exist_ok=True)
    
    downloading_message = await message.reply("Downloading the YouTube video, please wait...")

    try:
        # Download the video
        video_path = download_youtube_video(yt_url, download_path)
        
        # Send the video file to the user
        await client.send_video(chat_id=message.chat.id, video=video_path)
        
        # Delete the video file from the local storage
        os.remove(video_path)
        
    except Exception as e:
        await message.reply(f"An error occurred: {e}")

    # Delete the downloading message
    await client.delete_messages(chat_id=message.chat.id, message_ids=[downloading_message.id])

    # Clean up the download directory
    shutil.rmtree(download_path)
