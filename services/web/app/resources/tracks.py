from flask_restful import Resource, reqparse
from flask import make_response

from app.models import Playlist, Track


parser = reqparse.RequestParser()
parser.add_argument(
    "name",
    dest="name",
    location="args",
    required=False,
)
parser.add_argument(
    "spotify_id",
    dest="spotify_id",
    location="args",
    required=False,
)


class SearchTracks(Resource):
    def get(self):

        args = parser.parse_args()

        if args.name:
            track = Track.query.filter_by(name=args.name).first()

        if args.spotify_id:
            track = Track.query.filter_by(spotify_id=args.spotify_id).first()

        if track:
            return {
                "id": track.id,
                "spotify_id": track.spotify_id,
                "name": track.name,
            }
        else:
            return {}


class TrackPlaylists(Resource):
    def get(self, track_spotify_id):

        track = Track.query.filter_by(spotify_id=track_spotify_id).first()

        if track is None:
            return {}, 404

        playlists = track.get_playlists()

        return make_response({"playlists": [p.as_dict() for p in playlists]})
