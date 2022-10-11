from flask_restful import Resource, reqparse
from flask import make_response
from sqlalchemy.sql.expression import func

from app.models import Track


parser = reqparse.RequestParser()
parser.add_argument(
    "name",
    dest="name",
    location="args",
    required=False,
)
parser.add_argument(
    "spotifyID",
    dest="spotify_id",
    location="args",
    required=False,
)
parser.add_argument(
    "page",
    dest="page",
    location="args",
    required=False,
)


class SearchTracks(Resource):
    def get(self):

        args = parser.parse_args()
        tracks_query = None

        if args.spotify_id:
            track = Track.query.filter_by(spotify_id=args.spotify_id).first()
            if track:
                return track.as_json()
            else:
                return {"message": "No such track"}, 404

        if args.name:
            tracks_query = Track.query.filter(Track.name.ilike(f"%{args.name}%")).order_by(func.length(Track.name))
            count = tracks_query.count()

        if not tracks_query:
            return {}

        if args.page:
            tracks_out = tracks_query.paginate(int(args.page), 20, False)
            return {
                "count": count,
                "tracks": [track.as_json() for track in tracks_out.items],
            }
        # deprecated
        # only used on the v1 page
        else:
            if count < 50:
                tracks_out = [track.as_json() for track in tracks_query.all()]
            else:
                tracks_out = []
            return {
                "count": count,
                "tracks": tracks_out,
            }

        return {}


class TrackPlaylists(Resource):
    def get(self, track_spotify_id):

        track = Track.query.filter_by(spotify_id=track_spotify_id).first()

        if track is None:
            return {}, 404

        playlists_query = track.playlists_query()

        args = parser.parse_args()
        if args.page:
            playlists = playlists_query.paginate(int(args.page), 20, False).items
        else:
            playlists = playlists_query.all()

        return make_response({"playlists": [p.as_json() for p in playlists]})
