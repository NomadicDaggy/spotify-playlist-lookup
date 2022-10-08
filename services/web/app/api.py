from flask_restful import Api

from app.resources.test import Test
from app.resources.playlists import Playlists
from app.resources.simple_stats import SimpleStats
from app.resources.tracks import SearchTracks, TrackPlaylists

api = Api(prefix="/api/v1")  # Note, no app

api.add_resource(Test, "/test", "/test/<string:id>")
api.add_resource(Playlists, "/playlists")
api.add_resource(SimpleStats, "/simple-stats")
api.add_resource(SearchTracks, "/tracks")
api.add_resource(TrackPlaylists, "/tracks/<string:track_spotify_id>/playlists")
