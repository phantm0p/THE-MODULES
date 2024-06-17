# BOT/handlers/hangman_handler.py
from ..bot import bot
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.enums import ParseMode
import random

# List of words to guess with categories as hints
WORDS_WITH_HINTS = [
    ("python", "Programming Language"),
    ("telegram", "Messaging App"),
    ("pyrogram", "Telegram API Library"),
    ("hangman", "Classic Word Game"),
    ("bot", "Automated Program")
]

# Hangman stages
HANGMAN_PICS = [
    "😄",  # 0 wrong guesses
    "😐",  # 1 wrong guess
    "😕",  # 2 wrong guesses
    "😟",  # 3 wrong guesses
    "😢",  # 4 wrong guesses
    "😭",  # 5 wrong guesses
    "💀"   # 6 wrong guesses - Game Over
]

# Initialize a new Hangman game
@bot.on_message(filters.command("hangman"))
async def hangman_start(client, message):
    word, hint = random.choice(WORDS_WITH_HINTS)
    
    # Reveal the first letter and one other random letter
    revealed_indices = set([0])  # Start with the first letter revealed
    while len(revealed_indices) < 2:  # Ensure we reveal at least 2 letters
        revealed_indices.add(random.randint(0, len(word) - 1))
    
    state = "".join([ch if i in revealed_indices else "_" for i, ch in enumerate(word)])
    incorrect_guesses = 0
    guessed_letters = [word[i] for i in revealed_indices]
    
    # Store the game state
    game_data = {
        "word": word,
        "state": state,
        "incorrect_guesses": incorrect_guesses,
        "guessed_letters": guessed_letters,
        "hint": hint,
        "user_id": message.from_user.id  # Track the user who started the game
    }
    
    # Generate inline keyboard with letters
    buttons = generate_letter_buttons(guessed_letters)
    
    await message.reply(
        f"Let's play Hangman!\n\n<b>Hint</b>: {hint}\n\nWord: {state}\n\n{HANGMAN_PICS[incorrect_guesses]}",
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode=ParseMode.HTML  # Ensure HTML is parsed correctly
    )
    
    # Store the game state in a temporary dictionary (could use a database or more persistent storage)
    client.hangman_games[message.chat.id] = game_data

# Handle letter selection
@bot.on_callback_query(filters.regex(r"^letter_"))
async def handle_letter_selection(client, callback_query: CallbackQuery):
    letter = callback_query.data.split("_")[1]
    chat_id = callback_query.message.chat.id
    
    if chat_id not in client.hangman_games:
        await callback_query.answer("Game not found. Start a new game with /hangman.")
        return
    
    game_data = client.hangman_games[chat_id]
    if callback_query.from_user.id != game_data["user_id"]:
        await callback_query.answer("You are not allowed to play this game.")
        return
    
    word = game_data["word"]
    state = game_data["state"]
    incorrect_guesses = game_data["incorrect_guesses"]
    guessed_letters = game_data["guessed_letters"]
    hint = game_data["hint"]
    
    if letter in guessed_letters:
        await callback_query.answer("You already guessed that letter.")
        return
    
    guessed_letters.append(letter)
    
    if letter in word:
        state = "".join([letter if letter == ch else state[i] for i, ch in enumerate(word)])
    else:
        incorrect_guesses += 1
    
    # Check game status
    if state == word:
        await callback_query.message.edit_text(f"🎉 Congratulations! You guessed the word: {word}")
        client.hangman_games.pop(chat_id)
    elif incorrect_guesses >= len(HANGMAN_PICS) - 1:
        await callback_query.message.edit_text(f"💀 Game Over! The word was: {word}")
        client.hangman_games.pop(chat_id)
    else:
        buttons = generate_letter_buttons(guessed_letters)
        await callback_query.message.edit_text(
            f"<b>Hint</b>: {hint}\n\nWord: {state}\n\n{HANGMAN_PICS[incorrect_guesses]}",
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=ParseMode.HTML
        )
        game_data["state"] = state
        game_data["incorrect_guesses"] = incorrect_guesses
        game_data["guessed_letters"] = guessed_letters

# Utility function to generate inline keyboard buttons for letters
def generate_letter_buttons(disabled_letters=None):
    if disabled_letters is None:
        disabled_letters = []
        
    buttons = []
    for i in range(0, 26, 3):
        row = []
        for j in range(3):
            letter = chr(65 + i + j).lower()
            if letter in disabled_letters:
                row.append(InlineKeyboardButton(f"• {letter.upper()} •", callback_data=f"disabled_{letter}"))
            else:
                row.append(InlineKeyboardButton(letter.upper(), callback_data=f"letter_{letter}"))
        buttons.append(row)
    return buttons

# Initialize hangman game storage in the bot instance
bot.hangman_games = {}
