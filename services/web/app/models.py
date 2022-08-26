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


playlist_track = db.Table(
    "playlist_track",
    db.Column("playlist_id", db.Integer, db.ForeignKey("playlist.id")),
    db.Column("track_id", db.Integer, db.ForeignKey("track.id")),
)


class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spotify_id = db.Column(db.String(22), index=True, unique=True, nullable=False)


class Track(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spotify_id = db.Column(db.String(22), index=True, unique=True, nullable=False)
    name = db.Column(db.String(200), index=True, unique=True, nullable=False)
