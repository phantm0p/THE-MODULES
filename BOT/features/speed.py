# BOT/features/speed.py

import asyncio
import speedtest
from BOT.config import OWNER_ID  # Ensure OWNER_ID is correctly defined in your config

async def perform_speedtest():
    """
    Perform a speed test to measure download, upload speeds, and ping.

    Returns:
        tuple: (download_speed in Mbps, upload_speed in Mbps, ping in ms)
    """
    loop = asyncio.get_event_loop()
    s = speedtest.Speedtest()
    
    download_speed = await loop.run_in_executor(None, s.download)
    upload_speed = await loop.run_in_executor(None, s.upload)
    
    results = s.results.dict()
    download_speed = results["download"] / 10**6  # Convert from bits/s to Mbit/s
    upload_speed = results["upload"] / 10**6  # Convert from bits/s to Mbit/s
    ping = results["ping"]
    
    return download_speed, upload_speed, ping

async def handle_speedtest(client, message):
    """
    Handle the /spt command to perform a speed test.

    Args:
        client (Client): The Pyrogram client instance.
        message (Message): The message object triggering the command.

    Returns:
        None
    """
    if message.from_user.id != OWNER_ID:
        await message.reply_text("You are not authorized to use this command.")
        return
    
    try:
        download_speed, upload_speed, ping = await perform_speedtest()
        
        result_message = (
            f"DOWNLOAD SPEED: {download_speed:.2f} Mbps\n"
            f"UPLOAD SPEED: {upload_speed:.2f} Mbps\n"
            f"PING: {ping:.2f} ms"
        )
        
        await message.reply_text(result_message)
    
    except Exception as e:
        await message.reply_text(f"Failed to perform speedtest: {str(e)}")
        # Optionally log the exception if you have a logging setup
        print(f"Error performing speedtest: {e}")
