import os
import yt_dlp
from youtubesearchpython.__future__ import VideosSearch

from bot.config import config

os.makedirs(config.DOWNLOADS_DIR, exist_ok=True)


async def search_track(query: str) -> dict | None:
    """Search YouTube and return basic info of the first result."""
    search = VideosSearch(query, limit=1)
    result = await search.next()
    if not result["result"]:
        return None
    video = result["result"][0]
    return {
        "title": video["title"],
        "duration": video.get("duration", "Live"),
        "link": video["link"],
        "thumbnail": video["thumbnails"][0]["url"].split("?")[0],
        "channel": video["channel"]["name"],
    }


def download_audio(url: str) -> str:
    """Download audio from a YouTube link and return the local file path."""
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{config.DOWNLOADS_DIR}/%(id)s.%(ext)s",
        "quiet": True,
        "no_warnings": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file_path = f"{config.DOWNLOADS_DIR}/{info['id']}.mp3"
        return file_path
