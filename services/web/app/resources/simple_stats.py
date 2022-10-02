from flask_restful import Resource

from app.models import Playlist, Track


class SimpleStats(Resource):
    def get(self):
        playlist_count = Playlist.query.count()
        track_count = Track.query.count()
        return {
            "playlistCount": playlist_count,
            "trackCount": track_count,
        }
