# SOURCE https://github.com/Team-ProjectCodeX
# CREATED BY https://t.me/O_okarma
# API BY https://www.github.com/SOME-1HING
# PROVIDED BY https://t.me/ProjectCodeX

# <============================================== IMPORTS =========================================================>
import aiohttp
from pyrogram import Client, filters
from pyrogram.types import Message
from BOT.bot import bot

# <=======================================================================================================>

# <================================================ FUNCTIONS =====================================================>
async def get_cosplay_data():
    cosplay_url = "https://sugoi-api.vercel.app/cosplay"
    async with aiohttp.ClientSession() as session:
        async with session.get(cosplay_url) as response:
            return await response.json()

@bot.on_message(filters.command("cosplay") & filters.group)
async def cosplay_command(client: Client, message: Message):
    try:
        data = await get_cosplay_data()
        photo_url = data.get("url")  # Corrected key: "url" instead of "cosplay_url"
        if photo_url:
            await message.reply_photo(photo=photo_url)
        else:
            await message.reply_text("Could not fetch photo URL.")
    except aiohttp.ClientError:
        await message.reply_text("Unable to fetch data.")

# <================================================ END =======================================================>
