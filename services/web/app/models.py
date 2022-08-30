from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __repr__(self):
        return "<User {}>".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class PlaylistTrack(db.Model):
    __tablename__ = "playlist_track"

    id = db.Column(db.Integer, primary_key=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey("playlists.id"))
    track_id = db.Column(db.Integer, db.ForeignKey("tracks.id"))

    track = db.relationship("Track", back_populates="playlists")
    playlist = db.relationship("Playlist", back_populates="tracks")

    def __repr__(self):
        return f"{self.playlist_id} {self.track_id}"


class Playlist(db.Model):
    __tablename__ = "playlists"

    id = db.Column(db.Integer, primary_key=True)
    spotify_id = db.Column(db.String(22), index=True, unique=True, nullable=False)
    tracks_last_refreshed_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now(),
        server_onupdate=db.func.now(),
    )

    tracks = db.relationship("PlaylistTrack", back_populates="playlist")


class Track(db.Model):
    __tablename__ = "tracks"

    id = db.Column(db.Integer, primary_key=True)
    spotify_id = db.Column(db.String(22), index=True, unique=True, nullable=False)
    name = db.Column(db.String(200), index=True, nullable=False)

    playlists = db.relationship("PlaylistTrack", back_populates="track")

    def __repr__(self):
        return f"Track {self.id} {self.spotify_id} {self.name}"

    def get_playlists(self, search_term: str):
        """search_term is an exact song name"""
        return (
            db.session.query(Playlist)
            .filter(Playlist.id == PlaylistTrack.playlist_id)
            .filter(Track.id == PlaylistTrack.track_id)
            .filter(Track.name == search_term)
            .all()
        )


# TODO: insert_playlist_tracks() does a bit too much and should be split.
#
# Maybe it should be coupled to the db model classes? Maybe as a wrapper around
# them with a new separate __init__ function for each model class, so that
# you could create and insert a new Track, just by calling Track(playlist_dict).add().commit()
# or something like that. ...But then you would have to specify the dict many times, so rather
# better would be a class for the playlist object from the api, so like ApiPlaylist.insert_all()
# But I still don't like the coupling between the API data and the database model...
def insert_playlists_tracks(playlist_dict):
    """Inserts a playlist with tracks in the database

    Example Input:
    {
        "id": "0" * 22,
        "tracks": [
            {"id": "0" * 22, "name": "track0"},
            {"id": "1" * 22, "name": "track1"},
            {"id": "2" * 22, "name": "track2"}]}

    Inserts playlist, tracks and playlist-track relationships
    """

    # Add playlist
    playlist_id = playlist_dict["id"]
    if Playlist.query.filter_by(spotify_id=playlist_id).count() == 0:
        p = Playlist(spotify_id=playlist_id)
        db.session.add(p)
        db.session.flush()
    else:
        p = Playlist.query.filter_by(spotify_id=playlist_id).first()

    # Add tracks
    tracks_to_add = []
    for track in playlist_dict["tracks"]:

        track_sid = track["id"]
        # For each new track that should be inserted, check that that track is not already
        # in the database.
        #
        # This will be very inefficient for large numbers of Tracks, but is fine for now.
        #
        # A better way might be letting the database just reject duplicate
        # tracks and continue on, but I had trouble getting it to work, since
        # session.rollback rolls back the whole session, i.e. this whole test function.
        #
        # An alternative and also better way might be to gather all the tracks in a list
        # and filter all at once for duplicates in the database. Then add only non-dupes, but
        # save the dupes for PlaylistTrack adding later.
        #
        # TODO: how to efficiently check dupes in list against database table?
        if Track.query.filter_by(spotify_id=track_sid).count() == 0:
            t = Track(spotify_id=track_sid, name=track["name"])
            db.session.add(t)
            db.session.flush()
        else:
            t = Track.query.filter_by(spotify_id=track_sid).first()

        tracks_to_add.append(t)

    # Add relationships
    for track in tracks_to_add:
        r = PlaylistTrack(playlist_id=p.id, track_id=track.id)
        db.session.add(r)

    db.session.commit()
