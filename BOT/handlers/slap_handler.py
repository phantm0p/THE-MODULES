import random
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message
from BOT.bot import bot
from BOT.imgs_config import SLAP_IMAGES  # Assuming you have a list of slap images

# Command handler for /slap
@bot.on_message(filters.command("slap") & filters.group)
async def slap_command(client: Client, message: Message):
    if not message.reply_to_message and len(message.command) < 2:
        await message.reply_text("You need to reply to a user's message or provide a username to slap them.")
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

    # Check if the bot is being slapped
    bot_id = (await client.get_me()).id
    if user_b.id == bot_id:
        await message.reply_text("Hey, don't slap me! I'm just a bot.")
        return

    if user_a.id == user_b.id:
        await message.reply_text("You cannot slap yourself. That's weird.")
        return

    # Get a random slap image URL
    slap_image_url = random.choice(SLAP_IMAGES)

    # Send the slap message with the image
    await client.send_photo(
        chat_id=message.chat.id,
        photo=slap_image_url,
        caption=f"👋 **[{user_a.first_name}](tg://user?id={user_a.id})** slapped **[{user_b.first_name}](tg://user?id={user_b.id})**! That must've hurt! 💥",
        parse_mode=ParseMode.MARKDOWN
    )
