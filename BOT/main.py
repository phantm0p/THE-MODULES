# BOT/main.py

from .bot import bot
import logging
from .handlers import *  # Import all handlers

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    bot.run()
