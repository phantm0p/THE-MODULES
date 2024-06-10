# managing_handlers/ban_handler.py
from pyrogram import filters
from pyrogram.types import Message
from ..config import DEV_USERS
from pyrogram.enums import ChatMemberStatus
from ..managing.ban import ban_user, unban_user
from ..bot import bot  # Import the bot instance

def can_restrict(func):
    async def non_admin(client, message: Message):
        if message.from_user.id in DEV_USERS:
            return await func(client, message)

        check = await client.get_chat_member(message.chat.id, message.from_user.id)
        if check.status not in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
            return await message.reply_text(
                "» You're not an admin, Please stay in your limits."
            )

        admin = check.privileges
        if admin and admin.can_restrict_members:
            return await func(client, message)
        else:
            return await message.reply_text(
                "`You don't have permissions to restrict users in this chat."
            )

    return non_admin

@bot.on_message(filters.command("ban") & filters.group)
@can_restrict
async def handle_ban(client, message: Message):
    args = message.command[1:]
    
    if len(args) == 0 and not message.reply_to_message:
        return await message.reply_text("Reply to a user's message or provide a username/user_id to ban them.")
    
    user_id = None
    user = None
    
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        user = message.reply_to_message.from_user
    elif args:
        if args[0].startswith("@"):
            user = await client.get_users(args[0])
            user_id = user.id
        elif args[0].isdigit():
            user_id = int(args[0])
            user = await client.get_users(user_id)
    
    if not user_id:
        return await message.reply_text("Invalid username or user_id.")
    
    await ban_user(client, message, user_id, user)

@bot.on_message(filters.command("unban") & filters.group)
@can_restrict
async def handle_unban(client, message: Message):
    args = message.command[1:]
    
    if len(args) == 0 and not message.reply_to_message:
        return await message.reply_text("Reply to a user's message or provide a username/user_id to unban them.")
    
    user_id = None
    user = None
    
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        user = message.reply_to_message.from_user
    elif args:
        if args[0].startswith("@"):
            user = await client.get_users(args[0])
            user_id = user.id
        elif args[0].isdigit():
            user_id = int(args[0])
            user = await client.get_users(user_id)
    
    if not user_id:
        return await message.reply_text("Invalid username or user_id.")
    
    await unban_user(client, message, user_id, user)
