from yt_dlp import YoutubeDL

def search_youtube(query):
    with YoutubeDL({"quiet": True}) as ydl:
        info = ydl.extract_info(f"ytsearch5:{query}", download=False)
        results = []
        for entry in info["entries"]:
            results.append({
                "title": entry["title"],
                "url": entry["webpage_url"]
            })
        return results