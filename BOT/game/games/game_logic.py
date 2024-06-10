# BOT/game/games/game_logic.py
import random
from ...game.gamedata import get_user, create_user, update_balance , save_gift_timestamps , get_gift_timestamps
from datetime import datetime, timedelta

INITIAL_BALANCE = 10000

def claim(user_id):
    user = get_user(user_id)
    if user:
        return "You have already claimed your initial balance."
    create_user(user_id, INITIAL_BALANCE)
    return f"€ {INITIAL_BALANCE} has been credited to your account."

def bet(user_id, amount, choice):
    user = get_user(user_id)
    if not user:
        return "You need to claim your initial balance first using /claim."

    balance = user['balance']
    if amount > balance:
        return "You don't have enough balance to place this bet."

    coin_result = random.choice(['heads', 'tails'])
    won = (choice == 'h' and coin_result == 'heads') or (choice == 't' and coin_result == 'tails')
    
    # Update balance immediately after placing the bet
    new_balance = balance - amount
    if won:
        new_balance += amount * 2
    
    update_balance(user_id, new_balance)

    result = "won" if won else "lost"
    if won:
        return f"The coin landed on {coin_result}. You {result} € {amount * 2}. Your new balance is € {new_balance}."
    else:
        return f"The coin landed on {coin_result}. You {result} € {amount}. Your new balance is € {new_balance}."
    

async def gift(client, sender_id, receiver_id, amount):
    # Check if the sender is trying to gift to themselves
    if sender_id == receiver_id:
        return False, "You cannot gift to yourself."
    
    # Check if the user has already gifted 5 times in the last hour
    if count_gifts_in_last_hour(sender_id) >= 5:
        return False, "You have exceeded the maximum limit of gifts in the last hour."

    # Check if the amount exceeds half of the sender's balance
    sender = get_user(sender_id)
    if not sender or amount > sender['balance'] / 2:
        return False, "You cannot gift more than half of your total balance."

    # Update the sender's balance
    update_balance(sender_id, sender['balance'] - amount)

    # Update the receiver's balance
    update_balance(receiver_id, get_user(receiver_id)['balance'] + amount)
    
    # Save the timestamp of the gift
    save_gift_timestamps(sender_id, datetime.now())
    
    receiver_info = await client.get_users(receiver_id)
    return True, f"You have gifted € {amount} to {receiver_info.first_name}."

def count_gifts_in_last_hour(sender_id):
    # Query the database to get the timestamps of gifts for the sender
    timestamps = get_gift_timestamps(sender_id)
    
    # Count the number of gifts within the last hour
    current_time = datetime.now()
    count = sum(1 for timestamp in timestamps if current_time - timestamp <= timedelta(hours=1))
    
    return count


async def handle_gift_reply(client, message):
    sender_id = message.from_user.id
    receiver_id = message.reply_to_message.from_user.id
    args = message.command[1:]
    if len(args) != 1 or not args[0].isdigit():
        return False, "Usage: /gift <amount>"

    amount = int(args[0])
    return await gift(client, sender_id, receiver_id, amount)

async def handle_gift_mention(client, message):
    sender_id = message.from_user.id
    args = message.command[1:]
    if len(args) != 2 or not args[1].isdigit():
        return False, "Usage: /gift @username <amount>"
    
    receiver_username = args[0]
    receiver_id = (await client.get_users(receiver_username)).id
    amount = int(args[1])
    return await gift(client, sender_id, receiver_id, amount)