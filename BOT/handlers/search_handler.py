# handlers/search_handler.py

from pyrogram import filters
from pyrogram.types import InputMediaPhoto, Message
from ..bot import bot
from ..state import state
import random

BINGSEARCH_URL = "https://sugoi-api.vercel.app/search"
NEWS_URL = "https://sugoi-api.vercel.app/news?keyword={}"

# /news command handler
@bot.on_message(filters.command("news"))
async def news(_, message: Message):
    keyword = message.text.split(" ", 1)[1].strip() if len(message.text.split()) > 1 else ""
    url = NEWS_URL.format(keyword)

    try:
        response = await state.get(url)
        news_data = response.json()

        if "error" in news_data:
            error_message = news_data["error"]
            await message.reply_text(f"Error: {error_message}")
        else:
            if len(news_data) > 0:
                news_item = random.choice(news_data)
                title = news_item["title"]
                excerpt = news_item["excerpt"]
                source = news_item["source"]
                relative_time = news_item["relative_time"]
                news_url = news_item["url"]
                message_text = f"𝗧𝗜𝗧𝗟𝗘: {title}\n𝗦𝗢𝗨𝗥𝗖𝗘: {source}\n𝗧𝗜𝗠𝗘: {relative_time}\n𝗘𝗫𝗖𝗘𝗥𝗣𝗧: {excerpt}\n𝗨𝗥𝗟: {news_url}"
                await message.reply_text(message_text)
            else:
                await message.reply_text("No news found.")

    except Exception as e:
        await message.reply_text(f"Error: {str(e)}")


# /bingsearch command handler
@bot.on_message(filters.command("bingsearch"))
async def bing_search(client, message: Message):
    try:
        if len(message.command) == 1:
            await message.reply_text("Please provide a keyword to search.")
            return

        keyword = " ".join(message.command[1:])
        params = {"keyword": keyword}

        response = await state.get(BINGSEARCH_URL, params=params)

        if response.status_code == 200:
            results = response.json()
            if not results:
                await message.reply_text("No results found.")
            else:
                message_text = ""
                for result in results[:7]:
                    title = result.get("title", "")
                    link = result.get("link", "")
                    message_text += f"{title}\n{link}\n\n"
                await message.reply_text(message_text.strip())
        else:
            await message.reply_text("Sorry, something went wrong with the search.")
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")
