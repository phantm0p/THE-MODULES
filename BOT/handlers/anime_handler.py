from pyrogram import filters
from pyrogram.types import Message
from ..bot import bot
from ..features.anime import get_anime_details, create_anime_image
from io import BytesIO

@bot.on_message(filters.command("anime"))
async def handle_anime(client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("Usage: /anime <anime_title>")
    
    anime_title = " ".join(message.command[1:])
    try:
        anime_details = get_anime_details(anime_title)
        image = create_anime_image(anime_details)
        image_byte_array = BytesIO()
        image.save(image_byte_array, format='JPEG')
        image_byte_array.seek(0)

        # Truncate the description to 30 words
        description = " ".join(anime_details['description'].split()[:30]) + "..."

        caption = (
            f"🔹 **{anime_details['title']['english'] or anime_details['title']['romaji'] or anime_details['title']['native']}**\n"
            f"🔸 **Type**: {anime_details['format']}\n"
            f"🔸 **Genres**: {', '.join(anime_details['genres'])}\n"
            f"🔸 **Average Rating**: {anime_details['averageScore']}\n"
            f"🔸 **Status**: {anime_details['status']}\n"
            f"🔸 **First Aired**: {anime_details['startDate']['day']}-{anime_details['startDate']['month']}-{anime_details['startDate']['year']}\n"
            f"🔸 **Last Aired**: {anime_details['endDate']['day']}-{anime_details['endDate']['month']}-{anime_details['endDate']['year']}\n"
            f"🔸 **Episodes**: {anime_details['episodes']}\n"
            f"🔸 **Duration**: {anime_details['duration']} minutes per episode\n"
            f"\n**Synopsis**:\n{description}"
        )
        
        await client.send_photo(message.chat.id, image_byte_array, caption=caption)
    except Exception as e:
        await message.reply_text(str(e))
