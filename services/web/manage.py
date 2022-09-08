from flask.cli import FlaskGroup

from app.models import User, db, insert_playlists_tracks, refresh_all_playlist_metadata
from app.api_data_import import MaterializedPlaylist
from app import create_app


app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command("seed_db")
def seed_db():
    user = User(
        email="example@gmail.com",
        username="admin",
    )
    user.set_password(app.config["DEFAULT_ADMIN_PASSWORD"])
    db.session.add(user)
    db.session.commit()

    for i in ["50CP5OXFyr6qmCX8wZoum5", "6tlAGIxetz8wFTHeVIvC0N"]:
        mp = MaterializedPlaylist(i)
        playlist_data = mp.get_data()
        insert_playlists_tracks(playlist_data)


@cli.command("refresh_playlists")
def refresh_playlists():
    refresh_all_playlist_metadata()


if __name__ == "__main__":
    cli()
