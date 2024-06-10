# managing/ban.py
from pyrogram import Client
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import Message

BAN_STICKER = "CAACAgUAAxkBAAEGWC5lloYv1tiI3-KPguoH5YX-RveWugACoQ4AAi4b2FQGdUhawbi91DQE"
UNBAN_STICKER = "CAACAgUAAxkBAAEGWC5lloYv1tiI3-KPguoH5YX-RveWugACoQ4AAi4b2FQGdUhawbi91DQE"

async def ban_user(client: Client, message: Message, user_id: int, user: object):
    chat_id = message.chat.id

    # Check if the user to be banned is an admin
    member_status = await client.get_chat_member(chat_id, user_id)
    if member_status.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
        return await message.reply_text("I can't ban admins.")

    try:
        await client.ban_chat_member(chat_id, user_id)
        await message.reply_sticker(BAN_STICKER)
        user_mention = f"[{user.first_name}](tg://user?id={user.id})" if user else f"[user](tg://user?id={user_id})"
        await message.reply_text(f"Banned {user_mention}!")
    except Exception as e:
        print(e)

async def unban_user(client: Client, message: Message, user_id: int, user: object):
    chat_id = message.chat.id

    try:
        await client.unban_chat_member(chat_id, user_id)
        await message.reply_sticker(UNBAN_STICKER)
        user_mention = f"[{user.first_name}](tg://user?id={user.id})" if user else f"[user](tg://user?id={user_id})"
        await message.reply_text(f"Unbanned {user_mention}!")
    except Exception as e:
        print(e)
