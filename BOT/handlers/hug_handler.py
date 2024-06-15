import random
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram.enums import ParseMode
from BOT.bot import bot
from BOT.imgs_config import HUG_IMAGES  # Assuming you have a similar list of hug images as for kiss images

# Command handler for /hug
@bot.on_message(filters.command("hug") & filters.group)
async def hug_command(client: Client, message: Message):
    if not message.reply_to_message and len(message.command) < 2:
        await message.reply_text("You need to reply to a user's message or provide a username to send a hug request.")
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
        await message.reply_text("No thanks, I don't need a hug right now.")
        return

    if user_a.id == user_b.id:
        await message.reply_text("You cannot send a hug request to yourself.")
        return

    # Create inline button for User B to accept
    inline_keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Accept", callback_data=f"accept_hug:{user_a.id}:{user_b.id}")]
        ]
    )

    # Send the hug request message
    await message.reply_text(
        f"🤗 **[{user_b.first_name}](tg://user?id={user_b.id})**, **[{user_a.first_name}](tg://user?id={user_a.id})** wants to send you a hug! 🤗\n\n"
        "Will you accept the hug?",
        reply_markup=inline_keyboard,
        parse_mode=ParseMode.MARKDOWN
    )

# Callback handler for accepting the hug
@bot.on_callback_query(filters.regex(r"^accept_hug:(\d+):(\d+)$"))
async def accept_hug_callback(client: Client, callback_query):
    data = callback_query.data.split(":")
    user_a_id = int(data[1])
    user_b_id = int(data[2])

    user_a = await client.get_users(user_a_id)
    user_b = await client.get_users(user_b_id)

    if callback_query.from_user.id != user_b.id:
        await callback_query.answer("Only the recipient can accept this hug request.", show_alert=True)
        return

    # Get a random hug image URL
    hug_image_url = random.choice(HUG_IMAGES)

    # Delete the acceptance message with the inline button
    await callback_query.message.delete()

    # Send the hug accepted message with the image
    await client.send_photo(
        chat_id=callback_query.message.chat.id,
        photo=hug_image_url,
        caption=f"💞 **[{user_b.first_name}](tg://user?id={user_b.id})** accepted the hug from **[{user_a.first_name}](tg://user?id={user_a.id})**! 💞",
        parse_mode=ParseMode.MARKDOWN
    )

    await callback_query.answer()
