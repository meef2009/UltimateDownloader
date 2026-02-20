import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

class SpotifyAPI:

    def __init__(self, client_id, client_secret):
        if client_id and client_secret:
            creds = SpotifyClientCredentials(
                client_id=client_id,
                client_secret=client_secret
            )
            self.sp = spotipy.Spotify(
                client_credentials_manager=creds
            )
        else:
            self.sp = None

    def search_track(self, query):
        if not self.sp:
            return []

        results = self.sp.search(q=query, type="track", limit=5)
        tracks = []

        for item in results["tracks"]["items"]:
            tracks.append({
                "name": item["name"],
                "artist": item["artists"][0]["name"],
                "url": item["external_urls"]["spotify"]
            })

        return tracks