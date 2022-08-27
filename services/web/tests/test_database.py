from app.models import User, Playlist, Track, PlaylistTrack


def test_insert_user(session):
    u = User(email="test@test.com", username="tester", active=True)
    session.add(u)
    session.commit()
    assert User.query.count() == 1


def test_no_users():
    assert User.query.count() == 0


def test_playlist_tracks(session):

    playlists = [Playlist(spotify_id="0" * 22), Playlist(spotify_id="1" * 22)]
    session.add_all(playlists)

    tracks = [
        Track(spotify_id="0" * 22, name="0"),
        Track(spotify_id="1" * 22, name="1"),
        Track(spotify_id="2" * 22, name="2"),
        Track(spotify_id="3" * 22, name="3"),
    ]
    session.add_all(tracks)

    session.commit()

    playlist_tracks = [
        PlaylistTrack(playlist_id=1, track_id=1),
        PlaylistTrack(playlist_id=1, track_id=2),
        PlaylistTrack(playlist_id=2, track_id=3),
        PlaylistTrack(playlist_id=2, track_id=4),
    ]
    session.add_all(playlist_tracks)

    session.commit()

    assert PlaylistTrack.query.count() == 4
