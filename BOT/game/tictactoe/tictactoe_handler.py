from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from ...bot import bot
from ...game.tictactoe.tictactoe_logic import TicTacToe
from ...game.gamedata import get_user, update_balance, create_user
import random

games = {}

def get_game_key(chat_id, user_id1, user_id2):
    """Create a unique key for each game based on chat_id and user IDs."""
    return f"{chat_id}_{min(user_id1, user_id2)}_{max(user_id1, user_id2)}"

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

    game_key = get_game_key(chat_id, challenger, opponent)

    if game_key in games:
        return await message.reply_text("A game is already in progress between these users in this chat.")

    games[game_key] = {'challenger': challenger}
    await message.reply_text(
        f"{message.reply_to_message.from_user.mention}, you have been challenged to a Tic-Tac-Toe game by {message.from_user.mention}.",
        reply_markup=get_accept_markup(challenger)
    )

@bot.on_callback_query(filters.regex(r'^accept_\d+$'))
async def accept_challenge(client: Client, query: CallbackQuery):
    opponent = query.from_user.id
    challenger_id = int(query.data.split('_')[1])
    chat_id = query.message.chat.id

    game_key = get_game_key(chat_id, challenger_id, opponent)

    if game_key not in games or games[game_key].get('challenger') != challenger_id:
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

    # Find the game key where the user is a participant
    game_key = None
    for key, game in games.items():
        if user_id in [game.players['X'], game.players['O']]:
            game_key = key
            break

    if game_key is None:
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
    elif not game.empty_squares():
        await notification_message.edit_text(
            "It's a tie!"
        )
        await query.message.edit_text(
            f"⚡️⚡️⚡️{challenger.first_name} 🆚 {opponent_user.first_name}⚡️⚡️⚡️",
            reply_markup=get_board_markup(game.board)
        )
        del games[game_key]
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

    # Find the game key where the user is a participant
    game_key = None
    for key, game in games.items():
        if user_id in [game.players['X'], game.players['O']]:
            game_key = key
            break

    if game_key is None:
        return await message.reply_text("You are not part of any ongoing game.")

    del games[game_key]
    await message.reply_text("The Tic-Tac-Toe game has been ended.")
