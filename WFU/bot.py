import logging
from telegram.ext import Application
from motor.motor_asyncio import AsyncIOMotorClient
from wupload import register_upload_command
from inlinerquery import register_inline_query_handler

# Configure logging
logging.basicConfig(level=logging.INFO)

# Database setup
mongo_client = AsyncIOMotorClient("mongodb+srv://darkth0ughtss00:loniko0908@music.njvuzcz.mongodb.net/?retryWrites=true&w=majority&appName=Music")
db = mongo_client["your_database_name"]
collection = db["your_collection_name"]

# Bot setup
application = Application.builder().token("6617412135:AAFi7k0BBdGhsoSLm9maa48Z-puqRwA1wvw").build()

# Register command and inline query handlers
register_upload_command(application, collection)
register_inline_query_handler(application, collection)

# Start the bot
application.run_polling()
