import logging
import os
from telegram.ext import Application, CommandHandler
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from truth_dare import truth, dare
from react_module import register_react_handler

# Load environment variables from a .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database setup
try:
    mongo_client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
    db = mongo_client[os.getenv("DB_NAME")]
    collection = db[os.getenv("COLLECTION_NAME")]
    logger.info("Successfully connected to the MongoDB database.")
except Exception as e:
    logger.error("Failed to connect to the MongoDB database: %s", e)
    raise

# Bot setup
try:
    application = Application.builder().token(os.getenv("BOT_TOKEN")).build()
    logger.info("Bot setup successful.")
except Exception as e:
    logger.error("Failed to setup the bot: %s", e)
    raise


# Register Truth or Dare command handlers
application.add_handler(CommandHandler("truth", truth))
application.add_handler(CommandHandler("dare", dare))

# Register React command handler
register_react_handler(application)

# Start the bot
try:
    application.run_polling()
    logger.info("Bot started and running.")
except Exception as e:
    logger.error("Failed to start the bot: %s", e)
    raise
