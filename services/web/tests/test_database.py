from app.models import User, Playlist, Track, PlaylistTrack, insert_playlists_tracks


def test_insert_user(session):

    u = User(email="test@test.com", username="tester", active=True)
    session.add(u)
    session.commit()

    assert User.query.count() == 1


def test_no_users():
    assert User.query.count() == 0


p_unique = {
    "id": "0" * 22,
    "name": "n1",
    "description": "d1",
    "image_url": "",
    "owner_name": "",
    "tracks": [
        {"id": "0" * 22, "name": "track0"},
        {"id": "1" * 22, "name": "track1"},
        {"id": "2" * 22, "name": "track2"},
    ],
}

p_partial_overlap_1 = {
    "id": "1" * 22,
    "name": "n2",
    "description": "d1",
    "image_url": "",
    "owner_name": "",
    "tracks": [
        {"id": "3" * 22, "name": "track3"},
        {"id": "4" * 22, "name": "track4"},
    ],
}

p_partial_overlap_2 = {
    "id": "2" * 22,
    "name": "n3",
    "description": "d1",
    "image_url": "",
    "owner_name": "",
    "tracks": [
        {"id": "3" * 22, "name": "track3"},
        {"id": "5" * 22, "name": "track5"},
    ],
}

p_full_overlap = {
    "id": "3" * 22,
    "name": "n4",
    "description": "d1",
    "image_url": "",
    "owner_name": "",
    "tracks": [
        {"id": "3" * 22, "name": "track3"},
        {"id": "5" * 22, "name": "track5"},
    ],
}


def test_insert_unique_playlist_tracks():

    insert_playlists_tracks(p_unique)

    assert PlaylistTrack.query.count() == 3


def test_insert_tracks_from_two_playlists():

    insert_playlists_tracks(p_unique)
    insert_playlists_tracks(p_partial_overlap_1)

    assert Track.query.count() == 5
    assert Playlist.query.count() == 2
    assert PlaylistTrack.query.count() == 5


def test_insert_fully_overlapping_tracks():

    insert_playlists_tracks(p_partial_overlap_2)

    insert_playlists_tracks(p_full_overlap)

    assert Track.query.count() == 2
    assert Playlist.query.count() == 2
    assert PlaylistTrack.query.count() == 4
