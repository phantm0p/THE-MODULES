# BOT/handlers/ytsearch_handler.py

from pyrogram import Client, filters
from ..features.ytsearch import download_audio_from_youtube, cleanup_file
from ..bot import bot

@bot.on_message(filters.command("song") & filters.text)
async def song_handler(client, message):
    query = " ".join(message.command[1:])
    if not query:
        await message.reply("Please provide the name of the song. Usage: /song {song name}")
        return
    
    await message.reply("Searching for the song...")
    
    try:
        # Search for the song on YouTube and download the audio
        audio_file, title = download_audio_from_youtube(query)
        await message.reply(f"Downloading audio for: {title}...")

        # Send the audio file to the user
        await message.reply_audio(audio=audio_file, title=title)

        # Clean up the temporary file
        cleanup_file(audio_file)
        
    except Exception as e:
        await message.reply(f"An error occurred: {e}")
