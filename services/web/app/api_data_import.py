import os
import httpx

import tekore as tk
from dotenv import load_dotenv


class MaterializedPlaylist:
    def __init__(self, playlist_id: str) -> None:

        # TODO: this should probably be done elsewhere and not on every call
        self.client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self.client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

        self.token = tk.request_client_token(self.client_id, self.client_secret)

        big_timeout_client = httpx.Client(timeout=60.0)
        big_timeout_sender = tk.SyncSender(big_timeout_client)
        self.spotify = tk.Spotify(self.token, sender=big_timeout_sender)

        self.playlist_id = playlist_id

    def _get_playlist_tracks_from_api(self) -> list[dict]:

        tracks = []
        offset = 0
        tracks_received = 100

        while tracks_received == 100:
            p = self.spotify.playlist_items(
                playlist_id=self.playlist_id, as_tracks=True, offset=offset
            )
            for t in p["items"]:
                if t["track"] is not None and t["track"]["id"] is not None:
                    tracks.append(t)

            tracks_received = len(p["items"])
            offset += 100

        return tracks

    def _format_track(self, track_api_dict: dict) -> dict:

        return {
            "id": track_api_dict["track"]["id"],
            "name": track_api_dict["track"]["name"],
        }

    def get_data(self, include_tracks=True) -> dict:

        p = self.spotify.playlist(
            self.playlist_id, fields="name,description,id,images.url,owner.display_name"
        )

        self.data = {
            "id": self.playlist_id,
            "name": p["name"],
            "description": p["description"],
            "owner_name": p["owner"]["display_name"],
        }

        self.data["image_url"] = ""
        if len(p["images"]) > 0:
            self.data["image_url"] = p["images"][0]["url"]

        if include_tracks:
            self.data["tracks"] = [
                self._format_track(t) for t in self._get_playlist_tracks_from_api()
            ]

        return self.data


if __name__ == "__main__":
    load_dotenv(".env.spotify")

    p = MaterializedPlaylist("14zAdYu5s1rNOz93ZBmocv")
    d = p.get_data()
    print(d["tracks"], len(d["tracks"]))
