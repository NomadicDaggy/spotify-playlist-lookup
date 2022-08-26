import os

import tekore as tk

from dotenv import load_dotenv


load_dotenv(".env.spotify")

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

token = tk.request_client_token(client_id, client_secret)
spotify = tk.Spotify(token)


def get_playlist_tracks(playlist_id):
    tracks = []
    offset = 0
    tracks_received = 100

    while tracks_received == 100:
        p = spotify.playlist_items(
            playlist_id=playlist_id, as_tracks=True, offset=offset
        )
        tracks.extend(p["items"])
        tracks_received = len(p["items"])
        offset += 100

    return tracks


t = get_playlist_tracks("50CP5OXFyr6qmCX8wZoum5")
print(len(t), t[0]["track"]["name"])
