import os
from yt_dlp import YoutubeDL
from app.logger import log

class Downloader:

    def __init__(self, config):
        self.config = config

    def download(self, url, progress_hook=None):
        log(f"Downloading: {url}")

        ydl_opts = {
            "format": "bestaudio",
            "progress_hooks": [progress_hook] if progress_hook else [],
            "outtmpl": os.path.join(
                self.config["download_path"],
                "%(title)s.%(ext)s"
            ),
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": self.config["audio_quality"]
            }]
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        log(f"Finished: {url}")