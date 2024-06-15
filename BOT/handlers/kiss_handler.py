import random
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram.enums import ParseMode
from BOT.bot import bot
from BOT.imgs_config import KISS_IMAGES

# Command handler for /kiss
@bot.on_message(filters.command("kiss") & filters.group)
async def kiss_command(client: Client, message: Message):
    if not message.reply_to_message and len(message.command) < 2:
        await message.reply_text("You need to reply to a user's message or provide a username to send a kiss request.")
        return

    user_a = message.from_user

    if message.reply_to_message:
        user_b = message.reply_to_message.from_user
    else:
        username = message.command[1]
        try:
            user_b = await client.get_users(username)
        except Exception as e:
            await message.reply_text(f"Could not find user {username}.")
            return

    # Check if the bot is replying to its own message
    bot_id = (await client.get_me()).id
    if user_b.id == bot_id:
        await message.reply_text("Fuck off, I don't want a kiss from you.")
        return

    if user_a.id == user_b.id:
        await message.reply_text("Why are you single? You know, nowadays everyone is committed except you!")
        return

    # Create inline button for User B to accept
    inline_keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Accept", callback_data=f"accept_kiss:{user_a.id}:{user_b.id}")]
        ]
    )

    # Send the kiss request message
    await message.reply_text(
        f"💞 **[{user_b.first_name}](tg://user?id={user_b.id})** see **[{user_a.first_name}](tg://user?id={user_a.id})** wants to kiss you! 💞\n\n"
        "Will you accept the kiss?",
        reply_markup=inline_keyboard,
        parse_mode=ParseMode.MARKDOWN
    )

# Callback handler for accepting the kiss
@bot.on_callback_query(filters.regex(r"^accept_kiss:(\d+):(\d+)$"))
async def accept_kiss_callback(client: Client, callback_query):
    data = callback_query.data.split(":")
    user_a_id = int(data[1])
    user_b_id = int(data[2])

    user_a = await client.get_users(user_a_id)
    user_b = await client.get_users(user_b_id)

    if callback_query.from_user.id != user_b.id:
        await callback_query.answer("Only the recipient can accept this kiss request.", show_alert=True)
        return

    # Get a random kiss image URL
    kiss_image_url = random.choice(KISS_IMAGES)

    # Delete the acceptance message with the inline button
    await callback_query.message.delete()

    # Send the kiss accepted message with the image
    await client.send_photo(
        chat_id=callback_query.message.chat.id,
        photo=kiss_image_url,
        caption=f"💓 **[{user_b.first_name}](tg://user?id={user_b.id})** accepted the kiss from **[{user_a.first_name}](tg://user?id={user_a.id})**! 💓",
        parse_mode=ParseMode.MARKDOWN
    )

    await callback_query.answer()

