import logging

from extensions import celery

from app.models import insert_playlists_tracks
from app.api_data_import import MaterializedPlaylist


LOGGER = logging.getLogger()


@celery.task
def process_data(playlist_ids):
    LOGGER.info("Processing data")
    for p in playlist_ids:
        mp = MaterializedPlaylist(p)
        # get track data from spotify api
        playlist_data = mp.get_data()
        # insert into database
        insert_playlists_tracks(playlist_data)
