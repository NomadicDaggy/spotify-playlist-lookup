from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy


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

    # id = db.Column(db.Integer, primary_key=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey("playlists.id"), primary_key=True)
    track_id = db.Column(db.Integer, db.ForeignKey("tracks.id"), primary_key=True)

    track = db.relationship("Track", back_populates="playlists")
    playlist = db.relationship("Playlist", back_populates="tracks")


class Playlist(db.Model):
    __tablename__ = "playlists"

    id = db.Column(db.Integer, primary_key=True)
    spotify_id = db.Column(db.String(22), index=True, unique=True, nullable=False)

    tracks = db.relationship("PlaylistTrack", back_populates="playlist")


class Track(db.Model):
    __tablename__ = "tracks"

    id = db.Column(db.Integer, primary_key=True)
    spotify_id = db.Column(db.String(22), index=True, unique=True, nullable=False)
    name = db.Column(db.String(200), index=True, nullable=False)

    playlists = db.relationship("PlaylistTrack", back_populates="track")


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
        p = Playlist.query.filter_by(spoftfy_id=playlist_id).first()

    # Add tracks
    tracks_to_add = []
    for track in playlist_dict["tracks"]:
        if Track.query.filter_by(spotify_id=track["id"]).count() == 0:
            tracks_to_add.append(Track(spotify_id=track["id"], name=track["name"]))
    db.session.add_all(tracks_to_add)
    db.session.flush()

    # Add relationships
    relationships_to_add = []
    for track in tracks_to_add:
        relationships_to_add.append(PlaylistTrack(playlist_id=p.id, track_id=track.id))
    db.session.add_all(relationships_to_add)
    db.session.commit()
