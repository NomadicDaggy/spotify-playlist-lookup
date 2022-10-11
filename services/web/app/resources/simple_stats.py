from flask_restful import Resource
from extensions import cache

from app.models import Playlist, Track


class SimpleStats(Resource):
    @cache.cached(timeout=600, key_prefix="simple-stats")
    def get(self):
        playlist_count = Playlist.query.count()
        track_count = Track.query.count()
        return {
            "playlistCount": playlist_count,
            "trackCount": track_count,
        }
