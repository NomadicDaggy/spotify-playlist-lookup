from app.models import User, Playlist, Track, PlaylistTrack, insert_playlists_tracks
from app.api_data_import import MaterializedPlaylist


def test_playlists_with_removed_songs_dont_crash_import():
    # TODO: This is not a good test, cause it actually calls the Spotify API
    # and is not guaranteed to fail in the future.
    # To make it good, we would need to catch and mock the call to the API,
    # send a fake, but reliable response back to this fn.
    mp = MaterializedPlaylist("7IQA1MzJcCiaXyDboKS9we")
    playlist_data = mp.get_data()
    insert_playlists_tracks(playlist_data)
