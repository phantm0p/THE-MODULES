#!/bin/bash

# Start the BOT/main.py script
python -m BOT.main &

# Start the WFU/bot.py script
python WFU/bot.py &

# Wait for both processes to complete
wait
