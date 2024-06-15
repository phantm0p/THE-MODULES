import re
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from motor.motor_asyncio import AsyncIOMotorCollection

# Regular expression for Telegraph image link validation
TELEGRAPH_REGEX = re.compile(r'https://telegra\.ph/file/[\w\d]+\.jpg')

RARITY_MAP = {
    1: '⚪️ Common',
    2: '🟣 Rare',
    3: '🟡 Legendary',
    4: '🟢 Medium'
}

async def handle_upload_command(update: Update, context: ContextTypes.DEFAULT_TYPE, collection: AsyncIOMotorCollection) -> None:
    args = context.args
    if len(args) != 4:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid format. Use: /upload Img_url character-name anime-name rarity-number")
        return

    telegraph_link, character_name, anime_name, rarity_number_str = args

    if not TELEGRAPH_REGEX.match(telegraph_link):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Please provide a valid Telegraph image link.")
        return

    try:
        rarity_number = int(rarity_number_str)
        rarity = RARITY_MAP[rarity_number]
    except (ValueError, KeyError):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid rarity number. Use 1 for Common, 2 for Rare, 3 for Legendary, 4 for Medium.")
        return

    try:
        existing_entry = await collection.find_one({'link': telegraph_link})

        if existing_entry:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="This link is already in the database.")
        else:
            max_id_doc = await collection.find_one(sort=[("id", -1)], projection={"id": True})
            new_id = (max_id_doc['id'] + 1) if max_id_doc else 1
            
            await collection.insert_one({
                'id': new_id,
                'link': telegraph_link,
                'character_name': character_name,
                'anime_name': anime_name,
                'rarity': rarity
            })
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Link has been uploaded to the database.")
    except Exception as e:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="An error occurred while accessing the database. Please try again later.")
        logging.error(f"Error during database operation: {e}")

async def upload_command(update: Update, context: ContextTypes.DEFAULT_TYPE, collection: AsyncIOMotorCollection):
    await handle_upload_command(update, context, collection)

def register_upload_command(application: Application, collection: AsyncIOMotorCollection):
    application.add_handler(CommandHandler('upload', lambda update, context: upload_command(update, context, collection)))
