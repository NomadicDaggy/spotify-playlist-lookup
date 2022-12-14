from flask.cli import FlaskGroup

from app.models import User, refresh_all_playlist_metadata

from app import create_app
from extensions import db

import tasks


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

    tasks.process_data.delay(
        [
            "50CP5OXFyr6qmCX8wZoum5",
            "6tlAGIxetz8wFTHeVIvC0N",
            "37i9dQZF1DZ06evO3KmLhR",
            "55KWsRVvW4i65Gr4evwEm6",
            "4UEdX1S5H1LWKIb7ttTG3d",
            "3S4bx7lw9hhwlLC9HpPs6c",
            "2aCLBh2HtE2Ir7jyRaxZbC",
        ]
    )


@cli.command("refresh_playlists")
def refresh_playlists():
    refresh_all_playlist_metadata()


if __name__ == "__main__":
    cli()
