import logging

from flask_restful import Resource, reqparse

import tasks


LOGGER = logging.getLogger()


parser = reqparse.RequestParser()
parser.add_argument(
    "playlist_ids",
    dest="playlist_ids",
    type=list,
    location="json",
    required=True,
)


class Playlists(Resource):
    def post(self):
        args = parser.parse_args()

        if args.playlist_ids:
            LOGGER.info(args.playlist_ids)
            tasks.process_data.delay(args.playlist_ids)
        else:
            return {"message": "Something went wrong"}, 400

        return {"message": "Playlists accepted"}, 201
