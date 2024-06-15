# BOT/handlers/translate_handler.py

from pyrogram import Client, filters
from pyrogram.types import Message
from ..utils.translate import GoogleTranslator
from ..bot import bot

# Initialize the translator
translator = GoogleTranslator()

# Command to translate text
@bot.on_message(filters.command("tr") & filters.reply)
async def translate_reply(client: Client, message: Message):
    try:
        args = message.text.split()
        if len(args) < 2:
            await message.reply_text("Usage: /translate <target_lang>")
            return

        target_lang = args[1]
        source_text = message.reply_to_message.text
        
        # Translate the text
        translated_text = translator.translate(source_text, lang_tgt=target_lang)
        await message.reply_text(f"Translated to {target_lang}:\n{translated_text}")

    except Exception as e:
        await message.reply_text(f"Error: {e}")




# Command to detect language and translate text
@bot.on_message(filters.command("translate") & filters.reply)
async def detect_and_translate(client: Client, message: Message):
    try:
        target_lang = "en"  # Default target language
        if len(message.command) > 1:
            target_lang = message.command[1]
        
        source_text = message.reply_to_message.text
        
        # Detect the source language
        detected_lang = translator.detect(source_text)
        
        # Translate the text
        translated_text = translator.translate(source_text, lang_tgt=target_lang, lang_src=detected_lang)
        await message.reply_text(f"Detected: {detected_lang}\nTranslated to {target_lang}:\n{translated_text}")

    except Exception as e:
        await message.reply_text(f"Error: {e}")
