# BOT/handlers/song_handler.py
from pyrogram import Client, filters
from ..features.song_suggestion import sp
from ..bot import bot 

@bot.on_message(filters.command("top_playlist"))
async def get_featured_playlists(client, message):
    try:
        # Fetch featured playlists
        featured_playlists = sp.featured_playlists(limit=5)
        response = "**Featured Playlists and Top Tracks:**\n\n"

        # Iterate over each playlist and fetch the top 10 tracks
        for playlist in featured_playlists['playlists']['items']:
            response += f"💿 **{playlist['name']}**\n"
            response += f"{playlist['description']}\n\n"

            # Fetch top 10 tracks from the playlist
            playlist_tracks = sp.playlist_tracks(playlist['id'], limit=10)
            for i, item in enumerate(playlist_tracks['items']):
                track = item['track']
                response += (
                    f"{i+1}. {track['name']} by {', '.join([artist['name'] for artist in track['artists']])}\n"
                )

            response += "\n"  # Add space between playlists

        await message.reply(response, disable_web_page_preview=True)

    except Exception as e:
        await message.reply(f"An error occurred: {e}")



@bot.on_message(filters.command("sp_daily"))
async def daily_recommendations(client, message):
    recommendations = sp.recommendations(seed_genres=['pop', 'rock'], limit=5)

    response = "**Daily Music Recommendations:**\n\n"
    for i, track in enumerate(recommendations['tracks']):
        response += (
            f"{i+1}. {track['name']} by {', '.join([artist['name'] for artist in track['artists']])}\n"
            f"[Listen on Spotify]({track['external_urls']['spotify']})\n\n"
        )

    await message.reply(response, disable_web_page_preview=True)


@bot.on_message(filters.command("sp_trending"))
async def trending_music(client, message):
    # Fetch global top 50 playlist (Spotify's playlist ID for global top 50)
    top_playlist_id = '37i9dQZEVXbMDoHDwVN2tF'
    playlist = sp.playlist_tracks(top_playlist_id, limit=10)

    response = "**Trending Tracks (Global Top 50):**\n\n"
    for i, item in enumerate(playlist['items']):
        track = item['track']
        response += (
            f"{i+1}. {track['name']} by {', '.join([artist['name'] for artist in track['artists']])}\n"
            f"[Listen on Spotify]({track['external_urls']['spotify']})\n\n"
        )

    await message.reply(response, disable_web_page_preview=True)


@bot.on_message(filters.command("sp_new"))
async def new_releases(client, message):
    new_releases = sp.new_releases(limit=5)

    response = "**New Album Releases:**\n\n"
    for album in new_releases['albums']['items']:
        response += (
            f"💿 {album['name']} by {', '.join([artist['name'] for artist in album['artists']])}\n"
            f"Release Date: {album['release_date']}\n"
            f"[Listen on Spotify]({album['external_urls']['spotify']})\n\n"
        )

    await message.reply(response, disable_web_page_preview=True)


@bot.on_message(filters.command("sp_genre"))
async def recommend_genre(client, message):
    genres = " ".join(message.command[1:])
    if not genres:
        await message.reply("Please provide a genre or list of genres.")
        return

    recommended_tracks = sp.recommendations(seed_genres=genres.split(), limit=5)

    response = f"**Recommendations for genres: {genres}**\n\n"
    for i, track in enumerate(recommended_tracks['tracks']):
        response += (
            f"{i+1}. {track['name']} by {', '.join([artist['name'] for artist in track['artists']])}\n"
            f"[Listen on Spotify]({track['external_urls']['spotify']})\n\n"
        )

    await message.reply(response, disable_web_page_preview=True)


@bot.on_message(filters.command("sp_artist_top"))
async def artist_top_tracks(client, message):
    artist_name = " ".join(message.command[1:])
    if not artist_name:
        await message.reply("Please provide an artist name.")
        return

    results = sp.search(q=f'artist:{artist_name}', type='artist', limit=1)
    if not results['artists']['items']:
        await message.reply(f"No artist found with the name {artist_name}.")
        return

    artist = results['artists']['items'][0]
    artist_id = artist['id']
    top_tracks = sp.artist_top_tracks(artist_id, country='US')['tracks']

    response = f"**Top Tracks by {artist['name']}**:\n\n"
    for i, track in enumerate(top_tracks[:5]):
        response += (
            f"{i+1}. **{track['name']}**\n"
            f"[Listen on Spotify]({track['external_urls']['spotify']})\n\n"
        )

    await message.reply(response, disable_web_page_preview=True)

@bot.on_message(filters.command("sp_country"))
async def top_tracks_country(client, message):
    country_code = " ".join(message.command[1:])
    if not country_code:
        await message.reply("Please provide a country code (e.g., US, GB).")
        return

    try:
        top_tracks = sp.playlist_tracks(f'37i9dQZEVXbMDoHDwVN2tF', market=country_code, limit=10)
    except Exception as e:
        await message.reply(f"Error: {e}")
        return

    response = f"**Top Tracks in {country_code.upper()}**:\n\n"
    for i, item in enumerate(top_tracks['items']):
        track = item['track']
        response += (
            f"{i+1}. {track['name']} by {', '.join([artist['name'] for artist in track['artists']])}\n"
            f"[Listen on Spotify]({track['external_urls']['spotify']})\n\n"
        )

    await message.reply(response, disable_web_page_preview=True)