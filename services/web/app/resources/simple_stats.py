from flask_restful import Resource

from app.models import Playlist, Track


class SimpleStats(Resource):
    def get(self):
        playlist_count = Playlist.query.count()
        track_count = Track.query.count()
        return {
            "playlist_count": playlist_count,
            "track_count": track_count,
        }
