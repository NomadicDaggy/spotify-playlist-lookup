import logging
import httpx
import os

from extensions import celery

import tekore as tk
import sqlalchemy as sq
import psycopg2

from app.models import insert_playlists_tracks, Playlist
from app.api_data_import import MaterializedPlaylist


LOGGER = logging.getLogger()


@celery.task
def process_data(playlist_ids):
    LOGGER.info("Processing data")

    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    token = tk.request_client_token(client_id, client_secret)

    big_timeout_client = httpx.Client(timeout=60.0)
    big_timeout_sender = tk.SyncSender(big_timeout_client)
    spotify = tk.Spotify(token, sender=big_timeout_sender)

    for p in playlist_ids:
        LOGGER.info(p)
        exists = Playlist.query.filter_by(spotify_id=p).count()
        if exists:
            LOGGER.info("...is a dupe")
            continue

        mp = MaterializedPlaylist(p, spotify=spotify)
        # get track data from spotify api
        try:
            playlist_data = mp.get_data()
        except (
            tk.NotFound,
            tk.ServiceUnavailable,
            sq.exc.DataError,
            sq.exc.IntegrityError,
            psycopg2.errors.UniqueViolation,
            psycopg2.errors.StringDataRightTruncation,
        ) as e:
            print(e)
            continue

        # insert into database
        insert_playlists_tracks(playlist_data)
