# BOT/handlers/ud_handler.py

import requests
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from ..bot import bot 

@bot.on_message(filters.command("ud"))
async def ud_handler(client, message):
    text = message.text[len("/ud "):]
    if not text:
        await message.reply_text("Please provide a term to search.")
        return

    response = requests.get(f"https://api.urbandictionary.com/v0/define?term={text}")
    if response.status_code != 200:
        await message.reply_text("There was an error contacting the Urban Dictionary API.")
        return

    results = response.json()
    try:
        definition = results["list"][0]["definition"]
        example = results["list"][0]["example"]
        reply_text = f'*{text}*\n\n{definition}\n\n_{example}_'
    except IndexError:
        reply_text = "No results found."

    await message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN)
