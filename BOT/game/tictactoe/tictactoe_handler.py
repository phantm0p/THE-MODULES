#tictactoe_handler.py

from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from ...bot import bot
from ...game.tictactoe.tictactoe_logic import TicTacToe
from ...game.gamedata import get_user, update_balance, create_user
import random

games = {}
active_chats = set()

def get_game_key(chat_id):
    """Create a unique key for each game based on chat_id."""
    return f"{chat_id}"

def get_board_markup(board):
    buttons = []
    for i in range(0, 9, 3):
        buttons.append([InlineKeyboardButton(text=board[j] if board[j] != ' ' else 'ㅤ', callback_data=str(j)) for j in range(i, i+3)])
    return InlineKeyboardMarkup(buttons)

def get_accept_markup(challenger_id):
    return InlineKeyboardMarkup([[InlineKeyboardButton("Accept", callback_data=f"accept_{challenger_id}")]])

@bot.on_message(filters.command("tictactoe") & filters.reply)
async def start_tictactoe(client: Client, message: Message):
    challenger = message.from_user.id
    opponent = message.reply_to_message.from_user.id
    chat_id = message.chat.id

    if challenger == opponent:
        return await message.reply_text("You cannot challenge yourself.")

    game_key = get_game_key(chat_id)

    if game_key in active_chats:
        return await message.reply_text("There is already an ongoing game in this chat.")

    active_chats.add(game_key)
    games[game_key] = {'challenger': challenger, 'opponent': opponent}
    await message.reply_text(
        f"{message.reply_to_message.from_user.mention}, you have been challenged to a Tic-Tac-Toe game by {message.from_user.mention}.",
        reply_markup=get_accept_markup(challenger)
    )

@bot.on_callback_query(filters.regex(r'^accept_\d+$'))
async def accept_challenge(client: Client, query: CallbackQuery):
    opponent = query.from_user.id
    challenger_id = int(query.data.split('_')[1])
    chat_id = query.message.chat.id

    game_key = get_game_key(chat_id)

    if game_key not in games or games[game_key].get('challenger') != challenger_id or games[game_key].get('opponent') != opponent:
        return await query.answer("Invalid challenge or you are not the challenged user.", show_alert=True)

    await query.message.delete()  # Delete the challenge message

    first_turn = random.choice(['X', 'O'])
    first_player_id = challenger_id if first_turn == 'X' else opponent
    first_player = await client.get_users(first_player_id)
    challenger = await client.get_users(challenger_id)
    opponent_user = await client.get_users(opponent)

    games[game_key] = TicTacToe(challenger_id, opponent)

    notification_message = await query.message.reply_text(
        f"Tic-Tac-Toe game started between {challenger.mention} and {opponent_user.mention}. {first_player.first_name}'s ({first_turn}) turn is first!"
    )

    game_message = await query.message.reply_text(
        f"⚡️⚡️⚡️{challenger.first_name} 🆚 {opponent_user.first_name}⚡️⚡️⚡️",
        reply_markup=get_board_markup(games[game_key].board)
    )

    games[game_key].game_message_id = game_message.id
    games[game_key].notification_message_id = notification_message.id
    games[game_key].challenger = challenger  # Store the challenger object
    games[game_key].opponent_user = opponent_user  # Store the opponent_user object

@bot.on_callback_query(filters.regex(r'^\d$'))
async def handle_move(client: Client, query: CallbackQuery):
    user_id = query.from_user.id
    chat_id = query.message.chat.id

    game_key = get_game_key(chat_id)

    if game_key not in games:
        return await query.answer("You are not part of this game.", show_alert=True)

    game = games[game_key]
    move = int(query.data)

    if user_id != game.players[game.current_turn]:
        return await query.answer("It's not your turn.", show_alert=True)

    if not game.make_move(move, game.current_turn):
        return await query.answer("Invalid move.", show_alert=True)

    game.switch_turn()

    notification_message = await client.get_messages(chat_id=query.message.chat.id, message_ids=[game.notification_message_id])
    notification_message = notification_message[0]

    challenger = game.challenger
    opponent_user = game.opponent_user

    if game.current_winner:
        winner_id = game.players[game.current_winner]
        winner = await client.get_users(winner_id)

        # Update the winner's balance
        user = get_user(winner_id)
        if not user:
            create_user(winner_id, 2000)
        else:
            update_balance(winner_id, user['balance'] + 2000)

        await notification_message.edit_text(
            f"{winner.first_name} wins and receives €2000!"
        )
        await query.message.edit_text(
            f"⚡️⚡️⚡️{challenger.first_name} 🆚 {opponent_user.first_name}⚡️⚡️⚡️",
            reply_markup=get_board_markup(game.board)
        )
        del games[game_key]
        active_chats.remove(game_key)
    elif not game.empty_squares():
        await notification_message.edit_text(
            "It's a tie!"
        )
        await query.message.edit_text(
            f"⚡️⚡️⚡️{challenger.first_name} 🆚 {opponent_user.first_name}⚡️⚡️⚡️",
            reply_markup=get_board_markup(game.board)
        )
        del games[game_key]
        active_chats.remove(game_key)
    else:
        next_player_id = game.players[game.current_turn]
        next_player = await client.get_users(next_player_id)
        await notification_message.edit_text(
            f"{next_player.first_name}'s turn ({game.current_turn})"
        )
        await query.message.edit_text(
            f"⚡️⚡️⚡️{challenger.first_name} 🆚 {opponent_user.first_name}⚡️⚡️⚡️",
            reply_markup=get_board_markup(game.board)
        )

@bot.on_message(filters.command("endtictactoe"))
async def end_tictactoe(client: Client, message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    game_key = get_game_key(chat_id)

    if game_key not in games:
        return await message.reply_text("You are not part of any ongoing game.")

    del games[game_key]
    active_chats.remove(game_key)
    await message.reply_text("The Tic-Tac-Toe game has been ended.")
