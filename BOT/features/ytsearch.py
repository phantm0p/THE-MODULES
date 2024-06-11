# BOT/features/ytsearch.py

import yt_dlp
import os
import uuid

def download_audio_from_youtube(query):
    # Create a unique filename
    unique_filename = f"{uuid.uuid4()}.mp3"
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': unique_filename,
        'quiet': True,  # Suppress yt-dlp output
        'noplaylist': True,  # Do not download playlists
        'default_search': 'ytsearch',  # Treat query as a YouTube search
        'max_downloads': 1,  # Download only the first result
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Download the best audio and extract it as mp3
            info_dict = ydl.extract_info(query, download=True)
            return unique_filename, info_dict.get('title', 'Unknown Title')
    except Exception as e:
        raise Exception(f"yt-dlp error: {e}")

def cleanup_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
