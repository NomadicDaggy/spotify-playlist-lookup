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
