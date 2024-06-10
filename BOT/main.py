# BOT/main.py

import logging
from .bot import bot
from .handlers import *  # Import all handlers
from .game.game_handler import commands  # Import game handlers
from .managing_handlers import *

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



if __name__ == "__main__":
    bot.run()
