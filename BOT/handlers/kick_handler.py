import random
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message
from BOT.bot import bot
from BOT.imgs_config import KICK_IMAGES  # Assuming you have a list of kick images

# Command handler for /kickk
@bot.on_message(filters.command("kickk") & filters.group)
async def kick_command(client: Client, message: Message):
    if not message.reply_to_message and len(message.command) < 2:
        await message.reply_text("You need to reply to a user's message or provide a username to kick them.")
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

    # Check if the bot is being kicked
    bot_id = (await client.get_me()).id
    if user_b.id == bot_id:
        await message.reply_text("Ouch! Kicking a bot is not nice.")
        return

    if user_a.id == user_b.id:
        await message.reply_text("You cannot kick yourself. That's just silly.")
        return

    # Get a random kick image URL
    kick_image_url = random.choice(KICK_IMAGES)

    # Send the kick message with the image
    await client.send_photo(
        chat_id=message.chat.id,
        photo=kick_image_url,
        caption=f"🥾 **[{user_a.first_name}](tg://user?id={user_a.id})** kicked **[{user_b.first_name}](tg://user?id={user_b.id})**! That must've hurt! 💥",
        parse_mode=ParseMode.MARKDOWN
    )
