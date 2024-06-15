# BOT/features/ytsearch.py

from youtubesearchpython import VideosSearch
import yt_dlp
import os

def search_song(song_name):
    videos_search = VideosSearch(song_name, limit=1)
    results = videos_search.result()['result']
    if results:
        video_url = results[0]['link']
        return video_url
    else:
        return None

def download_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info_dict)
        return filename.replace(".webm", ".mp3").replace(".m4a", ".mp3")
