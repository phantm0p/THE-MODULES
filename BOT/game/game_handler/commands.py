# BOT/game/game_handler/commands.py
from pyrogram import filters
from pyrogram.types import Message
from ...bot import bot
from ...game.games.game_logic import claim, bet , handle_gift_reply, handle_gift_mention
from ...game.gamedata import get_user, get_top_users 

@bot.on_message(filters.command("claim"))
async def handle_claim(client, message: Message):
    user_id = message.from_user.id
    response = claim(user_id)
    await message.reply_text(response)

@bot.on_message(filters.command("bet"))
async def handle_bet(client, message: Message):
    user_id = message.from_user.id
    args = message.command[1:]
    if len(args) != 2 or not args[0].isdigit() or args[1] not in ['h', 't', 'heads', 'tails']:
        return await message.reply_text("Usage: /bet <amount> <h/t/heads/tails>")

    amount = int(args[0])
    choice = args[1][0]  # 'h' or 't'
    response = bet(user_id, amount, choice)
    await message.reply_text(response)

@bot.on_message(filters.command("wallet"))
async def handle_wallet(client, message: Message):
    user_id = message.from_user.id
    user = get_user(user_id)
    if not user:
        return await message.reply_text("You need to claim your initial balance first using /claim.")

    balance = user['balance']
    await message.reply_text(f"Your current balance is € {balance}.")

@bot.on_message(filters.command("topboard"))
async def handle_topboard(client, message: Message):
    top_users = get_top_users()
    response = "🏆 --LEADERBOARD-- 🏆\n"
    for idx, user in enumerate(top_users, 1):
        user_info = await client.get_users(user['user_id'])
        first_name = user_info.first_name
        response += f"{idx}. {first_name} - € {user['balance']}\n"
    await message.reply_text(response)

@bot.on_message(filters.command("gift") & filters.group)
async def handle_gift_command(client, message: Message):
    if message.reply_to_message:
        success, response = await handle_gift_reply(client, message)
    else:
        success, response = await handle_gift_mention(client, message)

    if not success:
        await message.reply_text(response)
    else:
        await message.reply_text(response)