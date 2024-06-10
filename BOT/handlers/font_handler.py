# BOT/handlers/font_handler.py

import os
from pyrogram import filters
from ..bot import bot
from ..features import font

# Command Handler: Apply Font Style
@bot.on_message(filters.command("font"))
async def font_handler(client, message):
    text = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else ""
    if not text:
        await message.reply_text("Please provide the text. Usage: /font {text}")
        return
    await message.reply_text(
        text,
        reply_markup=font.get_font_buttons(text),
        reply_to_message_id=message.id # Fix the attribute name here
    )

# Callback Query Handler: Apply Font Style
@bot.on_callback_query(filters.regex(r"^(bold|italic|underline|small_caps|outline|serif|comic|frozen|arrows|slash|upsidedown|fraktur|fantasy|monospace|futura|gaarmond|flaky|manga|luna|zebra|cursive):"))
async def font_callback(client, callback_query):
    style, text = callback_query.data.split(":", 1)
    new_text = font.apply_font(style, text)
    await callback_query.message.edit_text(
        new_text,
        reply_markup=font.get_font_buttons(text)
    )
    await callback_query.answer()
