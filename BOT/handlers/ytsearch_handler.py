# BOT/handlers/ytsearch_handler.py

from pyrogram import Client, filters
from ..features.ytsearch import search_song, download_audio
import os
from ..bot import bot 
@bot.on_message(filters.command("song"))
async def song_handler(client, message):
    if len(message.command) < 2:
        await message.reply_text("Please specify the name of the song.")
        return

    song_name = " ".join(message.command[1:])
    await message.reply_text(f"Searching for {song_name} on YouTube...")

    video_url = search_song(song_name)
    if not video_url:
        await message.reply_text("Song not found. Please try with a different name.")
        return

    await message.reply_text("Downloading the song...")
    file_path = download_audio(video_url)

    if file_path and os.path.exists(file_path):
        await message.reply_audio(audio=file_path, caption=f"Here is your song: {song_name}")
        os.remove(file_path)
    else:
        await message.reply_text("Failed to download the song. Please try again.")
