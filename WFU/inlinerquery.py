import logging
from telegram import InlineQueryResultPhoto, Update
from telegram.ext import Application, InlineQueryHandler, ContextTypes
from motor.motor_asyncio import AsyncIOMotorCollection

async def handle_inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE, collection: AsyncIOMotorCollection):
    query = update.inline_query
    search_text = query.query.strip()
    results = []

    try:
        search_criteria = {}
        if search_text:
            search_criteria = {'$or': [
                {'link': {'$regex': search_text, '$options': 'i'}},
                {'character_name': {'$regex': search_text, '$options': 'i'}},
                {'anime_name': {'$regex': search_text, '$options': 'i'}}
            ]}
        
        cursor = collection.find(search_criteria)

        async for document in cursor:
            caption = (
                f"🌸 <b>Name:</b> {document['character_name']}\n"
                f"🏖️ <b>Anime:</b> {document['anime_name']}\n"
                f"{document['rarity']} <b>Rarity</b>\n"
                f"🆔️ <b>Id:</b> {document['id']}"
            )
            results.append(
                InlineQueryResultPhoto(
                    id=str(document['_id']),
                    photo_url=document['link'],
                    thumbnail_url=document['link'],
                    title=document['character_name'],
                    description=f"{document['character_name']} from {document['anime_name']}",
                    caption=caption,
                    parse_mode="HTML"
                )
            )
    except Exception as e:
        logging.error(f"Error while processing inline query: {e}")
        results = []

    await context.bot.answer_inline_query(update.inline_query.id, results, cache_time=1)

async def inline_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, collection: AsyncIOMotorCollection):
    await handle_inline_query(update, context, collection)

def register_inline_query_handler(application: Application, collection: AsyncIOMotorCollection):
    application.add_handler(InlineQueryHandler(lambda update, context: inline_query_handler(update, context, collection)))
